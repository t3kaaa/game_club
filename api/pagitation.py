from rest_framework.pagination import PageNumberPagination

class ZonePagination(PageNumberPagination):
    page_size = 1

class RoomPagination(PageNumberPagination):
    page_size = 1

class DevicePagination(PageNumberPagination):
    page_size = 1
