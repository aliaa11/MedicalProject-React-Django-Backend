from rest_framework import generics
from accounts.models import Doctor
from .serializers import DoctorSerializer, DoctorWithAvailabilitySerializer
from django.http import HttpResponse
from datetime import date
def home(request):
    return HttpResponse("Welcome to the Medical API!")

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AvailableDoctorsListView(generics.ListAPIView):
    serializer_class = DoctorWithAvailabilitySerializer
    
    def get_queryset(self):
        today = date.today()
        available_doctors = Doctor.objects.filter(
            slots__isnull=False
        ).distinct()
        
        specialty = self.request.query_params.get('specialty', None)
        if specialty:
            available_doctors = available_doctors.filter(specialty=specialty)
            
        return available_doctors
