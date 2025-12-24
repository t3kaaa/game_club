from django.contrib import admin
from .models import *
from django.utils.html import format_html


admin.site.register(Zone)
admin.site.register(Room)
admin.site.register(Account)
admin.site.register(Device)



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('__str__','id', 'get_account_username', 'device', 'zone', 'start_time', 'end_time', 'colored_status','status')
    list_filter = ('status', 'zone')
    search_fields = ('account__user__username',)
    list_editable = ('status',)
    # readonly_fields = ('device', 'zone', 'start_time', 'end_time')
    
	
    def get_account_username(self, obj):
        return obj.account.user.username
    get_account_username.short_description = 'Username'
    get_account_username.admin_order_field = 'account__user__username'

    @admin.display(description="Booking holati")
    def colored_status(self, obj):
        colors = {
            'pending': 'gray',
            'active': 'blue',
            'finished': 'green',
            'missed': 'red',
            'cancelled':'pink'
        }
      
        status_str = str(obj.status).lower()
        return format_html(
            '<b style="color:{}">{}</b>',
            colors.get(status_str, 'black'),
            str(obj.status).upper()
        )

    def save_model(self, request, obj, form, change):
        if obj.status == 'active':

            
            if obj.device:
                obj.device.is_booked = True
                obj.device.save()

            
            if obj.room:
                obj.room.is_booked = True
                obj.room.save()

                Device.objects.filter(
                    room_id=obj.room
                ).update(is_booked=True)

     
        elif obj.status in ['finished', 'missed', 'cancelled']:

            if obj.device:
                obj.device.is_booked = False
                obj.device.save()

            if obj.room:
                obj.room.is_booked = False
                obj.room.save()

                Device.objects.filter(
                    room_id=obj.room
                ).update(is_booked=False)

        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        # Faqat superuser statusni o‘zgartira oladi
        return request.user.is_superuser	
    