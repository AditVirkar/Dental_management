from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('clinics/', views.clinic_list, name='clinic_list'),
    path('clinics/<int:clinic_id>/', views.clinic_detail, name='clinic_detail'),
    path('clinics/add/', views.add_clinic, name='add_clinic'),
    path('clinics/<int:clinic_id>/update_affiliations/', views.update_affiliations, name='update_affiliations'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('get-procedures/', views.get_procedures_by_doctor, name='get_procedures_by_doctor'),

    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/add-visit/', views.add_visit, name='add_visit'),
    path('patients/<int:patient_id>/schedule-appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('get-time-slots/', views.get_available_time_slots, name='get_time_slots'),


    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
