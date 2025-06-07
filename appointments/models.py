
# Create your models here.
from django.db import models
from doctors.models import Doctor
# from patients.models import Patient

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient_id = models.IntegerField(null=True, blank=True)  # مؤقتا رقم المريض فقط
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default='pending')  # مثل: pending, confirmed, canceled

    def __str__(self):
        return f"Appointment with Dr.{self.doctor.name} on {self.date} at {self.time}"

