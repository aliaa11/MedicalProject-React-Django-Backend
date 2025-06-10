from django.db import models
from accounts.models import Doctor

class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='slots')
    day = models.CharField(max_length=10)  # Saturday, Sunday, etc.
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.user.username} - {self.day} from {self.start_time} to {self.end_time}"
