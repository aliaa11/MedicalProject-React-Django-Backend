from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from appointments.models import Appointment
from availability.models import AvailabilitySlot
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, TokenError

class Command(BaseCommand):
    help = "Generate appointment slots for logged-in doctor based on availability slots"

    def add_arguments(self, parser):
        parser.add_argument('--token', type=str, help='JWT access token for the doctor')

    def get_next_date_for_day(self, day_number):
        today = datetime.today().date()
        today_weekday = today.weekday()  # Monday=0
        target_weekday = (int(day_number) - 1) % 7  # adjust if your system uses Sunday=0
        days_ahead = (target_weekday - today_weekday) % 7
        return today + timedelta(days=days_ahead)

    def handle(self, *args, **kwargs):
        token_str = kwargs['token']
        if not token_str:
            self.stdout.write(self.style.ERROR('Please provide a JWT token using --token'))
            return

        try:
            # Decode JWT
            token = AccessToken(token_str)
            user_id = token['user_id']
            User = get_user_model()
            user = User.objects.get(id=user_id)

            if not hasattr(user, 'doctor'):
                raise ValueError("Authenticated user is not a doctor")

            doctor = user.doctor
        except (TokenError, ValueError, User.DoesNotExist) as e:
            self.stdout.write(self.style.ERROR(f'Authentication Error: {str(e)}'))
            return

        # Get the availability slots for the doctor
        slots = AvailabilitySlot.objects.filter(doctor=doctor)
        created_count = 0

        for slot in slots:
            try:
                date = self.get_next_date_for_day(slot.day)  

                start = datetime.combine(date, slot.start_time)
                end = datetime.combine(date, slot.end_time)

                current = start
                while current + timedelta(minutes=30) <= end:
                    if not Appointment.objects.filter(
                        doctor=doctor,
                        date=date,
                        time=current.time()
                    ).exists():
                        Appointment.objects.create(
                            doctor=doctor,
                            date=date,
                            time=current.time(),
                            patient=None,
                            status='available'
                        )
                        created_count += 1
                    current += timedelta(minutes=30)
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error processing slot {slot.id}: {str(e)}"
                ))

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created_count} appointments for Dr. {doctor.user.get_full_name()}'
        ))
