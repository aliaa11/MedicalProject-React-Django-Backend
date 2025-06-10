from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from .views import create_user, create_doctor, create_patient, login_user



urlpatterns = [
    path('register/', create_user),
    path('register/doctor/', create_doctor),
    path('register/patient/', create_patient),

  path('login/', login_user, name='login'),  
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('patient/profile/', PatientProfileView.as_view(), name='patient-profile'),
    path('doctor/profile/', DoctorProfileView.as_view(), name='doctor-profile'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/users/', AllUsersView.as_view(), name='all-users'),
    path('admin/users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('admin/users/<int:user_id>/approve/', ApproveDoctor.as_view(), name='approve-doctor'),
    path('admin/users/<int:user_id>/reject/', RejectDoctor.as_view(), name='reject-doctor'),
    path('admin/users/<int:user_id>/delete/', DeleteUser.as_view(), name='delete-user'),
    path('admin/users/<int:user_id>/change-role/', ChangeUserRole.as_view(), name='change-user-role'),

    path('admin/specialties/', SpecialtyListView.as_view(), name='specialty-list'),
    path('admin/specialties/create/', SpecialtyCreateView.as_view(), name='specialty-create'),
    path('admin/specialties/<int:pk>/', SpecialtyUpdateDeleteView.as_view(), name='specialty-update-delete'),
   
]
