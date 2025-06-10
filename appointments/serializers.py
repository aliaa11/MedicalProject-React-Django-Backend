from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.username', read_only=True)
    doctor_specialty = serializers.CharField(source='doctor.specialty.name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'doctor_name', 'doctor_specialty', 'date', 'time', 'status']