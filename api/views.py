from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .models import Account,Zone,Room,Device,Booking
from .serializer import AccSerializer,ZoneSerializer, RoomSerializer, DevSerializer,BookSerializer,UserRegisterSerializer,UserLoginSerializer,BookingCancelSerializer,BookingHistorySerializer,BookRoomSerializer
from rest_framework.generics import ListCreateAPIView,CreateAPIView,DestroyAPIView,ListAPIView,RetrieveAPIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from django.contrib.auth import login
from .pagitation import ZonePagination,RoomPagination,DevicePagination,HistoryPagination




class Api_Account(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = request.user.account
        serializer = AccSerializer(account)
        return Response(serializer.data)

    def post(self, request):
        account = request.user.account
        amount = request.data.get('balance')

        if not amount:
            return Response(
                {"error": "amount yuborilmadi"},
                status=400
            )

        account.balance += float(amount)
        account.save()

        return Response({
            "message": "Balance to‘ldirildi",
            "balance": account.balance
        })


    
class Api_RegisterUser(ListCreateAPIView):   
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class Api_login(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.validated_data['username'])
        
        login(request, user)
        return Response(data=serializer.validated_data)
    
class Api_Zone(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

class Api_ZoneList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    pagination_class = ZonePagination

class Api_Room(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class Api_RoomList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoomSerializer
    pagination_class = RoomPagination

    def get_queryset(self):
        zone_id = self.request.query_params.get("zone_id")
        qs = Room.objects.all()
        if zone_id:
            qs = qs.filter(zone_id=zone_id)
        return qs

class Api_Device(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Device.objects.all()
    serializer_class = DevSerializer

class Api_AboutDevice(RetrieveAPIView):
    serializer_class = DevSerializer
    permission_classes = [IsAuthenticated]
    queryset=Device.objects.all()
    
class Api_AboutRoom(RetrieveAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    queryset=Room.objects.all()
    

class Api_DeviceList(ListAPIView):
    serializer_class = DevSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DevicePagination
    
    def get_queryset(self):
        zone_id = self.request.query_params.get("zone_id")
        qs = Device.objects.all()
        if zone_id:
            qs = qs.filter(zone_id=zone_id)
        return qs

class Api_DeviceBooking(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer

    def get_queryset(self):
        return Booking.objects.filter(
            device__isnull=False,
            account__user=self.request.user
        )
    
class Api_RoomBooking(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookRoomSerializer

    def get_queryset(self):
        return Booking.objects.filter(
            room__isnull=False,
            account__user=self.request.user
        )

class Api_BookingCancel(DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCancelSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Booking.objects.filter(account__user=self.request.user)
    
class Api_MyBookingHistory(ListAPIView):
    serializer_class = BookingHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class=HistoryPagination
    def get_queryset(self):
        return Booking.objects.filter(account__user=self.request.user).order_by('-start_time')
    
class All_Api(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        return Response({
            "accounts": AccSerializer(Account.objects.all(), many=True).data,
            "devices": DevSerializer(Device.objects.all(), many=True).data,
            "zones": ZoneSerializer(Zone.objects.all(), many=True).data,
            "bookings": BookSerializer(Booking.objects.all(), many=True).data,
        })