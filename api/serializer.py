from rest_framework import serializers
from .models import Account, Zone,Room,Device,Booking
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db import transaction


class AccSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Account
        fields = ['username', 'balance']

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'
    
    def create(self, validated_data):
        return Zone.objects.create(**validated_data)
    

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
    
    def create(self, validated_data):
        return Room.objects.create(**validated_data)
    

class DevSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
    
    def create(self, validated_data):
        return Device.objects.create(**validated_data)
    

class BookSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='account.user.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id','device', 'zone', 'start_time', 'end_time', 'status', 'accumulated_cost', 'played_minutes', 'username']
        read_only_fields = ['status', 'accumulated_cost', 'played_minutes', 'username']

    def validate(self, data):
        now=timezone.now()
        
        
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError({
                "non_field_errors": [
                    "Tugash vaqti boshlanish vaqtidan katta bo‘lishi kerak"
                ]
            })

        overlap = Booking.objects.filter(
            device=data['device'],
            status__in=['pending', 'active'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time'],
        ).exists()

        if overlap:
            raise serializers.ValidationError({
                "non_field_errors": [
                    "Bu PC bu vaqt oralig‘ida band"
                ]
            })

        if now > data['start_time']:
            raise serializers.ValidationError({
                "non_field_errors": [
                    "Boshlanish vaqti hozirgi vaqtdan katta bo‘lishi kerak"
                ]
            })


        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['account'] = request.user.account
        return Booking.objects.create(**validated_data, status='pending')
    
class BookingCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'status']
        read_only_fields = ['status']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.account.user != user:
            raise serializers.ValidationError("Siz bu bookingni bekor qila olmaysiz")
        if instance.status not in ['pending', 'active']:
            raise serializers.ValidationError("Faqat pending yoki active bookingni bekor qilish mumkin")
        
        instance.status = 'cancelled'
        instance.device.is_booked = False  
        instance.device.save()
        instance.save()
        return instance
    
class BookingHistorySerializer(serializers.ModelSerializer):
    device_type = serializers.CharField(source='device.type', read_only=True)
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    status = serializers.CharField()

    class Meta:
        model = Booking
        fields = ['device_type', 'zone_name', 'start_time', 'end_time', 'status', 'accumulated_cost', 'played_minutes']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username).first()
        if user is None:
            raise serializers.ValidationError({"username": "Invalid username"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Invalid password"})

        refresh = RefreshToken.for_user(user)

        return {
            "username": user.username,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    

class BookRoomSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='account.user.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id','room', 'zone','start_time', 'end_time','status', 'accumulated_cost','played_minutes', 'username']
        read_only_fields = ['status', 'accumulated_cost','played_minutes', 'username']

    def validate(self, data):
        now = timezone.now()

        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time start time dan katta bo‘lishi kerak")

        overlap = Booking.objects.filter(
            room=data['room'],
            status__in=['pending', 'active'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time'],
        ).exists()

        if overlap:
            raise serializers.ValidationError("Bu room bu vaqt oralig‘ida band")

        if now > data['start_time']:
            raise serializers.ValidationError("O‘tmish vaqtga booking qilib bo‘lmaydi")

        return data

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        account = request.user.account

        room = validated_data['room']


        booking = Booking.objects.create(account=account,status='pending',**validated_data)

        
        room.is_booked = True
        room.save(update_fields=['is_booked'])

        
        Device.objects.filter(room_id=room,is_booked=False).update(is_booked=True)

        return booking