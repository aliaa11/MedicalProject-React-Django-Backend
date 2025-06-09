from django.urls import path
from .views import RegisterView, PatientProfileView,DoctorProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
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
