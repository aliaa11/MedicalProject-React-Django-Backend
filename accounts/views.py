from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
# from .serializers import PatientProfileSerializer,DoctorProfileSerializer
from .models import User, Doctor, Patient, Specialty
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework.permissions import AllowAny
from accounts.models import Doctor
from .serializers import *
from .permissions import IsRoleAdmin
from rest_framework.exceptions import NotFound


# views.py
# from django.contrib.auth.models import User
from rest_framework.decorators import api_view

@api_view(['POST'])
def create_user(request):
    data = request.data
    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return Response({'message': 'User created successfully', 'user_id': user.id}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def create_doctor(request):
    data = request.data
    try:
        user = User.objects.get(id=data['user_id'])
        specialty = Specialty.objects.get(id=data['specialty_id'])
        Doctor.objects.create(
            user=user,
            specialty=specialty,
            gender=data['gender'],
            phone=data['phone'],
            bio=data['bio'],
            contact_email=data['contact_email'],
            years_of_experience=data.get('years_of_experience', 0),
        )
        return Response({'message': 'Doctor profile created'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def create_patient(request):
    data = request.data
    try:
        user = User.objects.get(id=data['user_id'])
        Patient.objects.create(
            user=user,
            gender=data['gender'],
            date_of_birth=data['date_of_birth'],
            address=data['address'],
            phone=data['phone'],
            disease=data.get('disease', ''),
            medical_history=data.get('medical_history', ''),
        )
        return Response({'message': 'Patient profile created'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

class PatientProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        print("Request user:", self.request.user)
        try:
            return Patient.objects.get(user=self.request.user)
        except Patient.DoesNotExist:
            print("Patient does not exist for this user.")
            raise NotFound("Patient profile not found.")


    
    
class DoctorProfileView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [AllowAny] 
    lookup_field = 'id' 


class AllDoctorsView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorProfileSerializer 
    permission_classes = [AllowAny]

class DoctorProfileUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Doctor.objects.get(user=self.request.user)


# 1. عرض كل المستخدمين
class AllUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsRoleAdmin]


# 2. عرض تفاصيل مستخدم (دكتور أو مريض)
class UserDetailView(APIView):
    permission_classes = [IsRoleAdmin]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)

            if user.role == 'doctor':
                doctor = Doctor.objects.get(user=user)
                serializer = DoctorDetailSerializer(doctor)
            elif user.role == 'patient':
                patient = Patient.objects.get(user=user)
                serializer = PatientDetailSerializer(patient)
            else:
                serializer = UserSerializer(user)

            return Response(serializer.data)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


# 3. الموافقة على دكتور
class ApproveDoctor(APIView):
    permission_classes = [IsRoleAdmin]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, role='doctor')
            user.is_approved = True
            user.save()
            return Response({"message": "Doctor approved successfully"})
        except User.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)


# 4. رفض / تعطيل دكتور
class RejectDoctor(APIView):
    permission_classes = [IsRoleAdmin]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, role='doctor')
            user.is_approved = False
            user.save()
            return Response({"message": "Doctor rejected successfully"})
        except User.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)


# 5. حذف مستخدم
class DeleteUser(APIView):
    permission_classes = [IsRoleAdmin]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


# 6. عرض كل التخصصات
class SpecialtyListView(generics.ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsRoleAdmin]


# 7. إنشاء تخصص جديد
class SpecialtyCreateView(generics.CreateAPIView):
    serializer_class = SpecialtySerializer
    permission_classes = [IsRoleAdmin]


# 8. تعديل / حذف تخصص
class SpecialtyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsRoleAdmin]


# 9. تغيير دور مستخدم
class ChangeUserRole(APIView):
    permission_classes = [IsRoleAdmin]

    def post(self, request, user_id):
        role = request.data.get('role')
        if role not in ['admin', 'doctor', 'patient']:
            return Response({"error": "Invalid role"}, status=400)

        try:
            user = User.objects.get(id=user_id)
            user.role = role
            user.save()
            return Response({"message": f"User role updated to {role}"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
