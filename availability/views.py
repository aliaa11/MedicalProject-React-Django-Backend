from rest_framework import viewsets
from .models import AvailabilitySlot
from .serializers import AvailabilitySlotSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

class AvailabilitySlotViewSet(viewsets.ModelViewSet):
    queryset = AvailabilitySlot.objects.all()
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
      
        user = self.request.user
        return AvailabilitySlot.objects.filter(doctor__user=user)

    def perform_create(self, serializer):
       
        serializer.save(doctor=self.request.user.doctor)

class DoctorAvailableSlotsPublicView(generics.ListAPIView):
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return AvailabilitySlot.objects.filter(doctor_id=doctor_id)
