from django.urls import path
from . import views

urlpatterns = [

# Home
path('', views.home, name='home'),

# About
path('about/', views.about, name='about'),

# Doctors
path('doctors/', views.doctors, name='doctors_list'),

# Departments
path('departments/', views.departments, name='departments'),

# Patient Registration
path(
    'patient_registration/',
    views.patient_registration,
    name='patient_registration'
),


# Appointment Booking
path(
    'appointment/',
    views.appointment,
    name='appointment'
),

# Appointment History
path(
    'appointment-history/',
    views.appointment_history,
    name='appointment_history'
),

# Medical Records
path(
    'medical_records/',
    views.medical_records,
    name='medical_records'
),

path(
    'medical_record/add/',
    views.add_medical_record,
    name='add_medical_record'
),

path(
    'medical_record/edit/<int:id>/',
    views.edit_medical_record,
    name='edit_medical_record'
),

path(
    'medical-record/delete/<int:id>/',
    views.delete_medical_record,
    name='delete_medical_record'
),

# Login Pages
path(
    'doctor-login/',
    views.doctor_login,
    name='doctor_login'
),

path(
    'admin-login/',
    views.admin_login,
    name='admin_login'
),

path(
    'patient-login/',
    views.patient_login,
    name='patient_login'
),

# Dashboards
path(
    'doctor-dashboard/',
    views.doctor_dashboard,
    name='doctor_dashboard'
),

path(
    'admin-dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
),
path('patients/', views.patient_list, name='patient_list'),

path(
    'patient-dashboard/',
    views.patient_dashboard,
    name='patient_dashboard'
),
path(
    'prescription/',
    views.prescription,
    name='prescription'
),

path(
    'profile-settings/',
    views.profile_settings,
    name='profile_settings'
),

# Logout
path(
    'logout/',
    views.user_logout,
    name='logout'
),
path(
    'appointments/',
    views.appointment_list,
    name='appointment_list'
),

path(
    'appointment/add/',
    views.add_appointment,
    name='add_appointment'
),

path(
    'appointment/edit/<int:id>/',
    views.edit_appointment,
    name='edit_appointment'
),

path(
    'appointment/delete/<int:id>/',
    views.delete_appointment,
    name='delete_appointment'
),
# Details Pages
path(
    'doctor/<int:id>/',
    views.doctor_detail,
    name='doctor_detail'
),
path(
    'appointment/approve/<int:id>/',
    views.approve_appointment,
    name='approve_appointment'
),
path(
    "admin-profile/",
    views.admin_profile,
    name="admin_profile"
),

path(
    'appointment/cancel/<int:id>/',
    views.cancel_appointment,
    name='cancel_appointment'
),
path('prescriptions/', views.prescription, name='prescriptions'),
path('prescription/add/', views.add_prescription, name='add_prescription'),
path('prescription/edit/<int:id>/', views.edit_prescription, name='edit_prescription'),
path('prescription/delete/<int:id>/', views.delete_prescription, name='delete_prescription'),
path('patients/', views.patient_list, name='patient_list'),
path('patient/add/', views.add_patient, name='add_patient'),
path('patient/edit/<int:id>/', views.edit_patient, name='edit_patient'),
path('patient/delete/<int:id>/', views.delete_patient, name='delete_patient'),
path('doctors/', views.doctor_list, name='doctor_list'),
path('doctor/add/', views.add_doctor, name='add_doctor'),
path('doctor/edit/<int:id>/', views.edit_doctor, name='edit_doctor'),
path('doctor/delete/<int:id>/', views.delete_doctor, name='delete_doctor'),
path(
    'department/<int:id>/',
    views.department_detail,
    name='department_detail'
),


]
