from django.urls import path
from .views import AppointmentListCreateView, BookAppointmentView, PatientAppointmentsView, AvailableAppointmentDaysView, AvailableAppointmentsByDayView
from accounts.views import DoctorProfileView


urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list'),
    path('book/<int:pk>/', BookAppointmentView.as_view(), name='book-appointment'),
    path('patient-appointments/', PatientAppointmentsView.as_view(), name='patient-appointments'),
    path('doctors/<int:doctor_id>/available-appointment-days/', AvailableAppointmentDaysView.as_view(), name='available-appointment-days'),
    path('doctors/<int:doctor_id>/available-appointments/', AvailableAppointmentsByDayView.as_view(), name='available-appointments-by-day'),
    path('doctors/<int:id>/', DoctorProfileView.as_view(), name='doctor-profile'),

]