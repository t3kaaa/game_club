from django.contrib import admin
from django.urls import path,include
from .views import Api_Account, Api_Zone, Api_Device, Api_Room, Api_DeviceBooking,All_Api,Api_DeviceList, Api_RoomList,Api_ZoneList,Api_RoomBooking,Api_RegisterUser,Api_login,Api_BookingCancel,Api_MyBookingHistory,Api_AboutDevice,Api_AboutRoom

urlpatterns = [
	path('all/', All_Api.as_view(),name='all'),
    path('account/', Api_Account.as_view() ,name="account"),

    path('zone/', Api_ZoneList.as_view(), name="zone"),
	path('room/', Api_RoomList.as_view(), name="room"),
	path('device/',Api_DeviceList.as_view(),name='device'),
	path('about_device/<int:pk>/',Api_AboutDevice.as_view(),name='about_device'),
	path('about_room/<int:pk>/',Api_AboutRoom.as_view(),name='about_room'),
	
    path('admin/zone/', Api_Zone.as_view(), name="zone"),
	path('admin/room/', Api_Room.as_view(), name="room"),
	path('admin/device/',Api_Device.as_view(),name='device'),
	
	path('booking_device/', Api_DeviceBooking.as_view(),name='booking_device'),
	path('booking_room/', Api_RoomBooking.as_view(),name='booking_room'),
	path('cancel_booking/<int:pk>/',Api_BookingCancel.as_view(),name='cancel'),
	path('my_bookings/', Api_MyBookingHistory.as_view(),name='history'),
	path('register/', Api_RegisterUser.as_view(),name="register"),
	path('login/',Api_login.as_view(), name=('login'))
]
