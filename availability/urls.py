from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailabilitySlotViewSet

router = DefaultRouter()
router.register(r'slots', AvailabilitySlotViewSet, basename='availabilityslot')

urlpatterns = [
    path('', include(router.urls)),
]
