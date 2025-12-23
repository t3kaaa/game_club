from django.contrib import admin
from django.urls import path,include
from .views import Api_Account, Api_Zone, Api_Device, Api_Room, Api_Booking,All_Api,Api_RegisterUser,Api_login,Api_BookingCancel,Api_MyBookingHistory

urlpatterns = [
	path('all/', All_Api.as_view(),name='all'),
    path('account/', Api_Account.as_view() ,name="account"),
    path('zone/', Api_Zone.as_view(), name="zone"),
	path('room/', Api_Room.as_view(), name="room"),
	path('device/',Api_Device.as_view(),name='device'),
	path('booking/', Api_Booking.as_view(),name='booking'),
	path('cancel_booking/<int:pk>/',Api_BookingCancel.as_view(),name='cancel'),
	path('my_bookings/', Api_MyBookingHistory.as_view(),name='history'),
	path('register/', Api_RegisterUser.as_view(),name="register"),
	path('login/',Api_login.as_view(), name=('login'))
]
