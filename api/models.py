from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Zone(models.Model):
    name = models.CharField(_("Zone name"), max_length=100)
    total_price = models.IntegerField(_("Total price"), default=0)
    image = models.ImageField(_("Image"), upload_to="zone/", blank=True, null=True)
    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(_("Room name"), max_length=70)
    description = models.CharField(_("Description"), max_length=255)
    zone_id = models.ForeignKey(Zone,on_delete=models.CASCADE,verbose_name=_("Zone"))
    is_booked = models.BooleanField(_("Is booked"), default=False)
    image = models.ImageField(_("Image"), upload_to="room/", blank=True, null=True)
    def __str__(self):
        return f"{self.name}_{self.zone_id.name} "


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='account',verbose_name=_("User"))
    balance = models.FloatField(_("Balance"), default=0)

    def __str__(self):
        return self.user.username


class Device(models.Model):

    DEVICE_TYPES = (("pc", _("PC")),("psg", _("PSG")),)

    type = models.CharField(_("Device type"),max_length=10,choices=DEVICE_TYPES)
    description = models.CharField(_("Description"),max_length=255,blank=True,null=True)
    devices = models.CharField(_("Devices"),max_length=255,blank=True,null=True)
    screen = models.CharField(_("Screen"),max_length=255,blank=True,null=True)
    image = models.ImageField(_("Image"), upload_to="devices/", blank=True, null=True)
    zone_id = models.ForeignKey(Zone,on_delete=models.CASCADE,verbose_name=_("Zone"))
    room_id = models.ForeignKey(Room,on_delete=models.SET_NULL,null=True,blank=True,verbose_name=_("Room"))
    is_booked = models.BooleanField(_("Is booked"), default=False)

    def __str__(self):
        return f"{self.get_type_display()} (ID:{self.id}, {self.zone_id.name})"


class Booking(models.Model):

    STATUS = (
        ("active", _("Active")),
        ("finished", _("Finished")),
        ("cancelled", _("Cancelled")),
        ("missed", _("Missed")),
        ("pending", _("Pending")),
    )

    device = models.ForeignKey(Device,on_delete=models.CASCADE,verbose_name=_("Device"),blank=True,null=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE,verbose_name=_("Room"),blank=True,null=True)
    zone = models.ForeignKey(Zone,on_delete=models.CASCADE,verbose_name=_("Zone"))
    account = models.ForeignKey(Account,on_delete=models.CASCADE,verbose_name=_("Account"))

    start_time = models.DateTimeField(_("Start time"))
    end_time = models.DateTimeField(_("End time"), blank=True, null=True)

    played_minutes = models.IntegerField(_("Played minutes"), default=0)
    accumulated_cost = models.FloatField(_("Accumulated cost"), default=0)

    status = models.CharField(_("Status"),max_length=20,choices=STATUS,default="pending")

    def __str__(self):
        return f"{self.account} | {self.device} | {self.get_status_display()}"
