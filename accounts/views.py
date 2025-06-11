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
from .serializers import *
from .permissions import IsRoleAdmin
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# views.py
# from django.contrib.auth.models import User
from rest_framework.decorators import api_view

@api_view(['POST'])
def create_user(request):
    data = request.data
    required_fields = ['username', 'email', 'password']
    
    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return Response(
            {'error': f'Missing required fields: {", ".join(missing_fields)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
        )
        user.role = data.get('role', 'patient')
        user.save()

        return Response(
            {'message': 'User created successfully', 'user_id': user.id}, 
            status=status.HTTP_201_CREATED
        )
    except IntegrityError as e:
        if 'username' in str(e):
            return Response(
                {'error': 'Username already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        elif 'email' in str(e):
            return Response(
                {'error': 'Email already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
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
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'message': 'يجب إدخال اسم المستخدم وكلمة المرور'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'message': 'بيانات الدخول غير صحيحة'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'تم تسجيل الدخول بنجاح',
        'role': user.role,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_id': user.id,
        'username': user.username,
        'email': user.email  # ✅ أضف هذا السطر
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def complete_registration(request):
    user_data = request.data.get('user_data')
    role = user_data.get('role')

    try:
        # 1. أنشئ المستخدم
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
        )
        user.role = role
        user.save()

        # 2. أنشئ الملف الشخصي بناءً على الدور
        if role == 'doctor':
            doctor_data = request.data.get('doctor_data')
            specialty = Specialty.objects.get(id=doctor_data['specialty_id'])
            Doctor.objects.create(
                user=user,
                specialty=specialty,
                gender=doctor_data['gender'],
                phone=doctor_data['phone'],
                bio=doctor_data['bio'],
                contact_email=doctor_data['contact_email'],
                years_of_experience=doctor_data.get('years_of_experience', 0),
            )
        elif role == 'patient':
            patient_data = request.data.get('patient_data')
            Patient.objects.create(
                user=user,
                gender=patient_data['gender'],
                date_of_birth=patient_data['date_of_birth'],
                address=patient_data['address'],
                phone=patient_data['phone'],
                disease=patient_data.get('disease', ''),
                medical_history=patient_data.get('medical_history', ''),
            )

        return Response({'message': 'Registration completed successfully'}, status=201)

    except Exception as e:
        # حذف المستخدم إذا فشل أي جزء
        if user and user.id:
            user.delete()
        return Response({'error': str(e)}, status=400)

class PatientProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Patient.objects.get(user=self.request.user)
        except Patient.DoesNotExist:
            raise NotFound("Patient profile not found")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        response_data = serializer.data
        response_data['user'] = {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email
        }
        
        return Response(response_data)
    
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


class DoctorByUserIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            doctor = Doctor.objects.get(user__id=user_id)
            serializer = DoctorProfileSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)

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
    permission_classes = [AllowAny]


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


        return Patient.objects.get(user=self.request.user)
    

class SpecialtyListView(generics.ListAPIView):
    serializer_class = SpecialtySerializer
    
    def get_queryset(self):
        queryset = Specialty.objects.all()
        
        # Get search parameters from query string
        search_term = self.request.query_params.get('search', None)
        exact_match = self.request.query_params.get('exact', None)
        
        if search_term:
            if exact_match:
                # Exact match search
                queryset = queryset.filter(name__iexact=search_term)
            else:
                # Partial match search (case-insensitive)
                queryset = queryset.filter(name__icontains=search_term)
        
        return queryset.order_by('name')
