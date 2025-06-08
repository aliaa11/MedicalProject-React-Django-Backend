from django.shortcuts import render
from rest_framework import generics, status
from .models import Appointment
from .serializers import AppointmentSerializer
from accounts.models import Patient
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import date
from availability.models import AvailabilitySlot
from django.db.models import Q


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer



class AvailableAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = date.today()
        queryset = Appointment.objects.filter(
            patient__isnull=True,
            date__gte=today
        )
        
        doctor_id = self.request.query_params.get('doctor_id', None)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
            
        return queryset


class BookAppointmentView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        appointment = self.get_object()
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient profile not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if appointment.patient is not None:
            return Response({'error': 'This appointment is no longer available.'}, status=status.HTTP_400_BAD_REQUEST)

        appointment.patient = patient
        appointment.status = 'pending'
        appointment.save()

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

class PatientAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            patient = Patient.objects.get(user=self.request.user)
            return Appointment.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            return Appointment.objects.none()
