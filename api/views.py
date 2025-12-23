from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .models import Account,Zone,Room,Device,Booking
from .serializer import AccSerializer,ZoneSerializer, RoomSerializer, DevSerializer,BookSerializer,UserRegisterSerializer,UserLoginSerializer,BookingCancelSerializer,BookingHistorySerializer
from rest_framework.generics import ListCreateAPIView,CreateAPIView,DestroyAPIView,ListAPIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from django.contrib.auth import login




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

class Api_Room(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class Api_Device(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Device.objects.all()
    serializer_class = DevSerializer

class Api_Booking(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Booking.objects.all()
    serializer_class = BookSerializer

class Api_BookingCancel(DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCancelSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Booking.objects.filter(account__user=self.request.user)
    
class Api_MyBookingHistory(ListAPIView):
    serializer_class = BookingHistorySerializer
    permission_classes = [IsAuthenticated]

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