from django.contrib import admin
from django.urls import path,include
from .views import Api_home
urlpatterns = [
    path('product/', Api_home,name="product"),
]
