from rest_framework import serializers
from .models import User, Doctor, Patient
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer
from availability.serializers import AvailabilitySlotSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('doctor', 'Doctor'), ('patient', 'Patient')])
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    gender = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    address = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    disease = serializers.CharField(required=False)
    medical_history = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'role', 'profile_picture',
            'gender', 'date_of_birth', 'address', 'phone', 'disease', 'medical_history'
        ]

    def create(self, validated_data):
        role = validated_data.pop('role')
        profile_picture = validated_data.pop('profile_picture', None)

        user = User.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
            role=role,
        )

        if role == 'doctor':
            Doctor.objects.create(user=user, contact_email=user.email)
        elif role == 'patient':
            Patient.objects.create(
                user=user,
                gender=validated_data.get('gender', ''),
                date_of_birth=validated_data.get('date_of_birth', None),
                address=validated_data.get('address', ''),
                phone=validated_data.get('phone', ''),
                disease=validated_data.get('disease', 'unknown'),
                medical_history=validated_data.get('medical_history', ''),
                profile_picture=profile_picture,
            )

        return user

class DoctorProfileSerializer(serializers.ModelSerializer):
    appointments = AppointmentSerializer(many=True, read_only=True)
    slots = AvailabilitySlotSerializer(many=True, read_only=True)
    
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'contact_email', 'specialty', 
            'gender', 'phone', 'bio', 'years_of_experience', 'profile_picture',
            'appointments', 'slots'
        ]

class AppointmentBriefSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'date', 'time', 'status']

class PatientProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    appointments = AppointmentBriefSerializer(many=True, read_only=True)
    profile_picture = serializers.ImageField(read_only=True)  
    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'gender', 'date_of_birth',
            'address', 'phone', 'disease', 'medical_history',
            'appointments', 'profile_picture'
        ]