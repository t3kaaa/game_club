
from django.core.management.base import BaseCommand
from django.utils import timezone
import time
from api.models import Booking


class Command(BaseCommand):
	help = 'Booking har 1 munitda ishlidi'
	
	def handle(self,*args,**options):
		self.stdout.write(self.style.SUCCESS("Booking worker ishga tushdi"))

		while True:
			now = timezone.now()
			# pending = Booking.objects.filter(status='pending',start_time__lt=now)


			# for book in pending:
			# 	book.status='active'
			# 	book.device.is_booked = True
			# 	book.device.save() 
			# 	book.save()




			active = Booking.objects.filter(status="active")

			for book in active:
				price_per_minute = book.zone.total_price / 60
				
				book.played_minutes += 1 
			
				book.accumulated_cost += price_per_minute

				if now >= book.end_time:
					book.status = 'finished'

					device = book.device
					device.is_booked = False
					device.save()

				book.save()

			auto_missed = Booking.objects.filter(
                status='pending',
                start_time__lt=now - timezone.timedelta(minutes=10)
            )


			missed= Booking.objects.filter(status='missed', start_time__lt=now - timezone.timedelta(minutes=15))

			

			for book in auto_missed:
				book.status = 'missed'
				book.save()


			time.sleep(60)
			print("Bir minut boldi ")