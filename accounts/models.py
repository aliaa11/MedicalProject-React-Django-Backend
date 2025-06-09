from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('doctor', 'Doctor'), ('patient', 'Patient'), ('admin', 'Admin')])
    is_approved = models.BooleanField(default=False)

def __str__(self):
     return self.username



class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    contact_email = models.EmailField()
    years_of_experience = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='doctors/', blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.username}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    disease = models.CharField(max_length=100, default="unknown")
    profile_picture = models.ImageField(upload_to='patients/', blank=True, null=True)
    medical_history	= models.TextField(blank=True)
    def __str__(self):
        return self.user.username
class Specialty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
