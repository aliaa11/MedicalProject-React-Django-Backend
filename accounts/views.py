from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PatientProfileSerializer,DoctorProfileSerializer
from .models import User, Doctor, Patient, Specialty
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework.permissions import AllowAny
from accounts.models import Doctor



class RegisterView(APIView):
    def post(self, request):
        data = request.data

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if not all([username, email, password, role]):
            return Response({"error": "Missing required fields"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        # Create user
        user = User.objects.create(
            username=username,
            email=email,
            role=role,
            password=make_password(password),
            is_approved=True  # أو False حسب نظامك
        )

        if role == 'doctor':
            Doctor.objects.create(
                user=user,
                specialty=Specialty.objects.get(id=data.get('specialty_id')),
                gender=data.get('gender'),
                phone=data.get('phone'),
                bio=data.get('bio', ''),
                contact_email=data.get('contact_email'),
                years_of_experience=data.get('years_of_experience', 0),
                profile_picture=data.get('profile_picture', None),
            )

        elif role == 'patient':
            Patient.objects.create(
                user=user,
                gender=data.get('gender'),
                date_of_birth=data.get('date_of_birth'),
                address=data.get('address'),
                phone=data.get('phone'),
                disease=data.get('disease', 'unknown'),
                medical_history=data.get('medical_history', ''),
                profile_picture=data.get('profile_picture', None),
            )


        return Response({"message": "User registered successfully"}, status=201)


class PatientProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Patient.objects.get(user=self.request.user)
    
    
class DoctorProfileView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [AllowAny]  # خليها حسب اللي يناسبك (مثلاً IsAuthenticated لو عايز حماية)
    lookup_field = 'id'  # أو 'pk' حسب الـ URL
