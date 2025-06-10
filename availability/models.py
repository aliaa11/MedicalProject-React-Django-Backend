from django.db import models
from accounts.models import Doctor  # تأكد الاستيراد صحيح

class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='slots')
    day = models.CharField(max_length=10)  # Saturday, Sunday, etc.
    start_time = models.TimeField()
    end_time = models.TimeField()

<<<<<<< HEAD
    def __str__(self):
        return f"{self.doctor.user.username} - {self.day} from {self.start_time} to {self.end_time}"
=======
    # def __str__(self):
    #     return f"{self.doctor.name} - {self.day} from {self.start_time} to {self.end_time}"
>>>>>>> 4574bf8 (get all available doctors. handling related issues)
