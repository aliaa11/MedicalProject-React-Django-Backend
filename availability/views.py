from rest_framework import viewsets
from .models import AvailabilitySlot
from .serializers import AvailabilitySlotSerializer
from rest_framework.permissions import IsAuthenticated

class AvailabilitySlotViewSet(viewsets.ModelViewSet):
    queryset = AvailabilitySlot.objects.all()
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
      
        user = self.request.user
        return AvailabilitySlot.objects.filter(doctor__user=user)

    def perform_create(self, serializer):
       
        serializer.save(doctor=self.request.user.doctor)
