from django.db import models
from django.conf import settings

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    specialty = models.CharField(max_length=100)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)
    bio = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
