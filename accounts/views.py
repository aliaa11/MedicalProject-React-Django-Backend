from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from .models import User, Doctor, Patient, Specialty
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .serializers import *
from .permissions import IsRoleAdmin



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
            is_approved=(role == 'patient')        )

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
