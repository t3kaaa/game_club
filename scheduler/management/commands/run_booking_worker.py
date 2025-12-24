
from django.core.management.base import BaseCommand
from django.utils import timezone
import time
from api.models import Booking


from django.core.management.base import BaseCommand
from django.utils import timezone
import time
from api.models import Booking, Device


class Command(BaseCommand):
    help = 'Booking har 1 minutda ishlaydi'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Booking worker ishga tushdi"))

        while True:
            now = timezone.now()

            active = Booking.objects.filter(status="active")

            for book in active:
                price_per_minute = book.zone.total_price / 60
                book.played_minutes += 1
                book.accumulated_cost += price_per_minute

                
                if now >= book.end_time:
                    book.status = 'finished'

                    if book.device:
                        book.device.is_booked = False
                        book.device.save()

                    if book.room:
                        book.room.is_booked = False
                        book.room.save()

                        Device.objects.filter(
                            room_id=book.room
                        ).update(is_booked=False)

                book.save()

        
            auto_missed = Booking.objects.filter(
                status='pending',
                start_time__lt=now - timezone.timedelta(minutes=10)
            )

            for book in auto_missed:
                book.status = 'missed'

                if book.device:
                    book.device.is_booked = False
                    book.device.save()

                if book.room:
                    book.room.is_booked = False
                    book.room.save()

                    Device.objects.filter(
                        room_id=book.room
                    ).update(is_booked=False)

                book.save()
            print("bir min boldi")
            time.sleep(60)
