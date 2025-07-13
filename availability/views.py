from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import AvailabilitySlot
from .serializers import AvailabilitySlotSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from accounts.models import Doctor

class AvailabilitySlotViewSet(viewsets.ModelViewSet):
    queryset = AvailabilitySlot.objects.all()
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'doctor'):
            return AvailabilitySlot.objects.filter(doctor=self.request.user.doctor)
        return AvailabilitySlot.objects.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'doctor'):
            serializer.save(doctor=self.request.user.doctor)
        else:
            raise PermissionDenied("Only doctors can create availability slots")

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, 'doctor'):
            return Response(
                {"detail": "Only doctors can create availability slots"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

class DoctorAvailableSlotsPublicView(generics.ListAPIView):
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            return AvailabilitySlot.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            return AvailabilitySlot.objects.none()