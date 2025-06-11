# # accounts/patient_serializers.py
# from rest_framework import serializers
# from .models import Patient
# from appointments.serializers import AppointmentBriefSerializer  # هذا لا يسبب دورة لأنه مبسط

# class PatientSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()
#     appointments = AppointmentBriefSerializer(many=True, read_only=True)

#     class Meta:
#         model = Patient
#         fields = [
#             'id', 'user', 'gender', 'date_of_birth',
#             'address', 'phone', 'disease', 'medical_history',
#             'appointments'
#         ]
