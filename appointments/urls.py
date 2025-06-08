from django.urls import path
from .views import AppointmentListCreateView, BookAppointmentView, PatientAppointmentsView, AvailableAppointmentsView


urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list'),
    path('book/<int:pk>/', BookAppointmentView.as_view(), name='book-appointment'),
    path('patient-appointments/', PatientAppointmentsView.as_view(), name='patient-appointments'),
    path('available/', AvailableAppointmentsView.as_view(), name='available-appointments'),

]