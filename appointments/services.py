# appointments/services.py
from datetime import datetime, timedelta
from appointments.models import Appointment
from availability.models import AvailabilitySlot

def generate_appointments_for_doctor(doctor):
    slots = AvailabilitySlot.objects.filter(doctor=doctor)
    created_count = 0

    for slot in slots:
        try:
            today = datetime.today().date()
            today_weekday = today.weekday()  # Monday=0
            target_weekday = (int(slot.day) - 1) % 7
            days_ahead = (target_weekday - today_weekday) % 7
            date = today + timedelta(days=days_ahead)

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
            print(f"Error processing slot {slot.id}: {str(e)}")

    return created_count
