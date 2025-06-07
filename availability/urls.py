from django.urls import path
from .views import AvailabilitySlotListCreateView

urlpatterns = [
    path('', AvailabilitySlotListCreateView.as_view(), name='availability-slot-list-create'),
]
