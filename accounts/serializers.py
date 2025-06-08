from rest_framework import serializers
from .models import User, Doctor, Patient

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('doctor', 'Doctor'), ('patient', 'Patient')])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data['role']
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=role,
        )

        # الربط حسب الدور
        if role == 'doctor':
            Doctor.objects.create(user=user, contact_email=user.email)  # ممكن نعدل البيانات لاحقًا
        elif role == 'patient':
            Patient.objects.create(user=user)

        return user
