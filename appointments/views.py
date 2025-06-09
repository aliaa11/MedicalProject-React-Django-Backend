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
from rest_framework.views import APIView
from django.db.models.functions import TruncDate
from .models import Appointment



class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer



class AvailableAppointmentDaysView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doctor_id):
        today = date.today()
        days_qs = Appointment.objects.filter(
            doctor_id=doctor_id,
            patient__isnull=True,
            date__gte=today
        ).values_list('date', flat=True).distinct().order_by('date')

        day_list = list(days_qs)
        day_list_str = [d.strftime('%Y-%m-%d') for d in day_list]

        return Response(day_list_str)

class AvailableAppointmentsByDayView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        date_str = self.request.query_params.get('date')  # متوقع 'YYYY-MM-DD'
        queryset = Appointment.objects.filter(
            doctor_id=doctor_id,
            patient__isnull=True
        )
        if date_str:
            queryset = queryset.filter(date=date_str)
        return queryset.order_by('time')


class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, doctor_id, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, doctor_id=doctor_id, patient__isnull=True)
        except Appointment.DoesNotExist:
            return Response({'detail': 'Appointment not available or already booked with this doctor.'}, status=404)

        appointment.patient = request.user.patient
        appointment.save()
        return Response({'detail': 'Appointment booked successfully.'})


class PatientAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            patient = Patient.objects.get(user=self.request.user)
            return Appointment.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            return Appointment.objects.none()

class UpdateAppointmentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, doctor__user=request.user)
        except Appointment.DoesNotExist:
            return Response({'detail': 'Appointment not found or you do not have permission.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status not in ['pending', 'confirmed', 'canceled']:
            return Response({'detail': 'Invalid status value.'}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = new_status
        appointment.save()
        return Response({'detail': f'Status updated to {new_status} successfully.'})        

