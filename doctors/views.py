from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Medical API!")

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
