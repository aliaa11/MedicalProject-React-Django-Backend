from django.urls import path
from .views import DoctorListCreateView, DoctorRetrieveUpdateDestroyView, AvailableDoctorsListView

urlpatterns = [
    path('', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view(), name='doctor-detail'),
    path('available-doctors/', AvailableDoctorsListView.as_view(), name="available doctors")
]
