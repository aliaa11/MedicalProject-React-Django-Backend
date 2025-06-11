from django.urls import path
from .views import AppointmentListCreateView, BookAppointmentView, PatientAppointmentsView, AvailableAppointmentDaysView, AvailableAppointmentsByDayView, UpdateAppointmentStatusView, AdminAppointmentDetailView, AdminAppointmentListView, DoctorAppointmentsView, AppointmentDetailView
# from accounts.views import DoctorProfileView


urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list'),
    path('doctor-appointments/', DoctorAppointmentsView.as_view(), name='doctor-appointments'),
    path('book/<int:doctor_id>/<int:pk>/', BookAppointmentView.as_view(), name='book-appointment'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('patient-appointments/', PatientAppointmentsView.as_view(), name='patient-appointments'),
    path('doctors/<int:doctor_id>/available-appointment-days/', AvailableAppointmentDaysView.as_view(), name='available-appointment-days'),
    path('doctors/<int:doctor_id>/available-appointments/', AvailableAppointmentsByDayView.as_view(), name='available-appointments-by-day'),
    path('update-status/<int:pk>/', UpdateAppointmentStatusView.as_view(), name='update-appointment-status'),
    path('admin/appointments/', AdminAppointmentListView.as_view(), name='admin-appointments-list'),
    path('admin/appointments/<int:pk>/', AdminAppointmentDetailView.as_view(), name='admin-appointment-detail'),
]