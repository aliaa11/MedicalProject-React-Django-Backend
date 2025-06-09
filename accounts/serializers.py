from rest_framework import serializers
from .models import User, Doctor, Patient, Specialty

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



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_approved']

class DoctorDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

class PatientDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = '__all__'

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name']
