from django.contrib import admin
from .models import User, Doctor, Specialty,Patient # استبدلي حسب أسماء الموديلات الموجودة عندك

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Specialty)
admin.site.register(Patient)  # إذا كان لديك موديل Patient أيضًا