from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailabilitySlotViewSet, DoctorAvailableSlotsPublicView

router = DefaultRouter()
router.register(r'slots', AvailabilitySlotViewSet, basename='availabilityslot')

urlpatterns = [
    path('', include(router.urls)),
    path('public/doctor/<int:doctor_id>/slots/', DoctorAvailableSlotsPublicView.as_view(), name='doctor-available-slots-public'),

]
