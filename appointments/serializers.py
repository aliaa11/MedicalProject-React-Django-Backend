from rest_framework import serializers
from .models import Appointment
# لا تستورد PatientDetailSerializer هنا

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = '__all__'

    def get_patient(self, obj):
        from accounts.serializers import PatientDetailSerializer  # استيراد مؤجل
        return PatientDetailSerializer(obj.patient).data
