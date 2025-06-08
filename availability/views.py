from django.shortcuts import render

# Create your views here.
# availability/views.py
from rest_framework import generics
from .models import AvailabilitySlot
from .serializers import AvailabilitySlotSerializer

class AvailabilitySlotListCreateView(generics.ListCreateAPIView):
    queryset = AvailabilitySlot.objects.all()
    serializer_class = AvailabilitySlotSerializer

