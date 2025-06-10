from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from appointments.models import Appointment
from availability.models import AvailabilitySlot

class Command(BaseCommand):
    help = "Generate appointment slots from availability slots"

    def get_next_date_for_day(self, day_name):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        today = datetime.today().date()
        today_weekday = today.weekday()
        target_weekday = days_of_week.index(day_name)
        days_ahead = target_weekday - today_weekday
        if days_ahead < 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)

    def handle(self, *args, **kwargs):
        slots = AvailabilitySlot.objects.all()
        for slot in slots:
            date = self.get_next_date_for_day(slot.day)
            start = datetime.combine(date, slot.start_time)
            end = datetime.combine(date, slot.end_time)

            current = start
            while current + timedelta(minutes=30) <= end:
                if not Appointment.objects.filter(
                    doctor=slot.doctor,
                    date=date,
                    time=current.time(),
                    patient__isnull=True
                ).exists():
                    Appointment.objects.create(
                        doctor=slot.doctor,
                        date=date,
                        time=current.time(),
                        patient=None,
                        status='pending'
                    )
                current += timedelta(minutes=30)

        self.stdout.write(self.style.SUCCESS('Appointments generated successfully.'))
