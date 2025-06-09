from django.contrib import admin
from .models import User, Doctor, Specialty,Patient 

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Specialty)
admin.site.register(Patient)  