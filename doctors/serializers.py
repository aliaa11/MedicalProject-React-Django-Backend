from rest_framework import serializers
# from .models import Doctor
from accounts.models import Doctor  
from availability.models import AvailabilitySlot
from availability.serializers import AvailabilitySlotSerializer

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorWithAvailabilitySerializer(serializers.ModelSerializer):
    slots = AvailabilitySlotSerializer(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialty', 'gender', 'phone', 'bio', 
                 'contact_email', 'years_of_experience', 'profile_picture',
                 'slots']