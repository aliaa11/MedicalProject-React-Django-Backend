from django.urls import path
from .views import RegisterView, PatientProfileView,DoctorProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('patient/profile/', PatientProfileView.as_view(), name='patient-profile'),
    path('doctor/profile/', DoctorProfileView.as_view(), name='doctor-profile'),  # <-- أضف ده لو عايز تعرض بروفايل الدكتور


]
