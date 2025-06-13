from django.db.models.signals import post_save
from django.dispatch import receiver
from availability.models import AvailabilitySlot
from django.core.management import call_command
from django.contrib.auth import get_user_model

@receiver(post_save, sender=AvailabilitySlot)
def generate_appointments_on_slot_change(sender, instance, created, **kwargs):
    """
    Signal to generate appointments when an availability slot is created or updated
    """
    User = get_user_model()
    doctor_user = instance.doctor.user
    
    # Generate a new JWT token for the doctor
    from rest_framework_simplejwt.tokens import AccessToken
    token = AccessToken.for_user(doctor_user)
    
    # Call the management command
    call_command('generate_appointments', token=str(token))