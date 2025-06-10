
# Create your models here.
from django.db import models
from accounts.models import Doctor
from accounts.models import Patient
# from patients.models import Patient

class Appointment(models.Model):
    doctor = models.ForeignKey('accounts.Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default='pending')  # مثل: pending, confirmed, canceled

    def __str__(self):
       return f"Appointment with Dr. {self.doctor.user.username} on {self.date} at {self.time}"


