from django.contrib import admin
from django.urls import path, include
from doctors.views import home

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doctors/', include('doctors.urls')),
    path('api/availability/', include('availability.urls')),
    path('', home, name='home'),
    path('api/appointments/', include('appointments.urls')),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),

]
