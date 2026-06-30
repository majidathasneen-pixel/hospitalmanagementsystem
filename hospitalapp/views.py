from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse

from .forms import PatientRegistrationForm, AppointmentForm,MedicalRecordForm,PrescriptionForm,PatientForm
from .models import( Patient, Appointment, MedicalRecord,Department,Doctor,Prescription)



# Home Page
def home(request):
    return render(request, 'home.html')


# About Page
def about(request):
    return render(request, 'about.html')


# Doctors Page
def doctors(request):
    return render(request, 'doctors.html')


# Departments Page
def departments(request):
    return render(request, 'departments.html')


# Patient Registration Page


def patient_registration(request):

    if request.method == "POST":

        form = PatientRegistrationForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username).exists():

                messages.error(request, "Username already exists.")

            else:

                user = User.objects.create_user(

                    username=username,

                    password=password,

                    email=form.cleaned_data["email"]

                )

                patient = form.save(commit=False)

                patient.user = user

                patient.save()

                messages.success(
                    request,
                    "Registration successful. Please login."
                )

                return redirect("patient_login")

    else:

        form = PatientRegistrationForm()

    return render(
        request,
        "patient_registration.html",
        {"form": form}
    )
def patient_list(request):

    patients = Patient.objects.all()

    return render(
        request,
        'patient_list.html',
        {'patients': patients}
    )

def add_patient(request):

    form = PatientRegistrationForm()

    if request.method == "POST":

        form = PatientRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('patient_list')

    return render(
        request,
        'add_patient.html',
        {'form': form}
    )


def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            return redirect('patient_list')

    else:
        form = PatientForm(instance=patient)

    return render(request, 'edit_patient.html', {
        'form': form
    })

def delete_patient(request, id):

    patient = Patient.objects.get(id=id)

    patient.delete()

    return redirect('patient_list')

    if form.is_valid():
        form.save()
        return redirect('patient_list')

    return render(
        request,
        'edit_patient.html',
        {'form': form}
    )

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {
        'doctors': doctors
    })


def add_doctor(request):
    if request.method == 'POST':
        Doctor.objects.create(
            name=request.POST['name'],
            specialization=request.POST['specialization'],
            phone=request.POST['phone'],
            email=request.POST['email']
        )
        return redirect('doctor_list')

    return render(request, 'add_doctor.html')

def edit_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == 'POST':
        doctor.name = request.POST['name']
        doctor.specialization = request.POST['specialization']
        doctor.phone = request.POST['phone']
        doctor.email = request.POST['email']
        doctor.save()

        return redirect('doctor_list')

    return render(request, 'edit_doctor.html', {
        'doctor': doctor
    })

def delete_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')

    return render(request, 'delete_doctor.html', {
        'doctor': doctor
    })
# Appointment Booking
def appointment(request):
    form = AppointmentForm()

    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = "Pending"   # Automatically set Pending
            appointment.save()

            messages.success(
                request,
                "Appointment booked successfully! Please wait for doctor's approval."
            )

            return redirect('appointment')

    return render(request, 'appointment.html', {'form': form})
def appointment_list(request):

    appointments = Appointment.objects.all()

    return render(
        request,
        'appointment_list.html',
        {'appointments': appointments}
    )
def approve_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    appointment.status = "Approved"
    appointment.save()

    return redirect('appointment_list')


def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    appointment.status = "Cancelled"
    appointment.save()

    return redirect('appointment_list')
def add_appointment(request):

    form = AppointmentForm()

    if request.method == 'POST':

        form = AppointmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('appointment_list')

    return render(
        request,
        'add_appointment.html',
        {'form': form}
    )
def edit_appointment(request, id):

    appointment = Appointment.objects.get(id=id)

    form = AppointmentForm(
        request.POST or None,
        instance=appointment
    )

    if form.is_valid():
        form.save()
        return redirect('appointment_list')

    return render(
        request,
        'edit_appointment.html',
        {'form': form}
    )
def delete_appointment(request, id):

    appointment = Appointment.objects.get(id=id)

    appointment.delete()

    return redirect('appointment_list')


# Appointment History
@login_required
def appointment_history(request):

    if not hasattr(request.user, 'patient'):
        return HttpResponse("Access Denied")

    patient = request.user.patient

    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')

    return render(request, 'appointment_history.html', {
        'appointments': appointments
    })


# Medical Records
def medical_records(request):

    # 👑 ADMIN
    if request.user.is_superuser or request.user.is_staff:
        records = MedicalRecord.objects.all()

    # 👨‍⚕️ DOCTOR
    elif hasattr(request.user, 'doctor'):
        doctor = request.user.doctor
        records = MedicalRecord.objects.filter(doctor=doctor)

    # 🧑‍🦰 PATIENT
    elif hasattr(request.user, 'patient'):
        patient = request.user.patient
        records = MedicalRecord.objects.filter(patient=patient)

    else:
        return HttpResponse("Access Denied")

    return render(request, 'medical_records.html', {
        'records': records,'is_doctor':hasattr(request.user,'doctor'),
    })

def add_medical_record(request):

    form = MedicalRecordForm()

    if request.method == 'POST':

        form = MedicalRecordForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('medical_records')

    return render(
        request,
        'add_medicalrecord.html',
        {'form': form}
    )

def edit_medical_record(request, id):

    record = MedicalRecord.objects.get(id=id)

    form = MedicalRecordForm(
        request.POST or None,
        instance=record
    )

    if form.is_valid():

        form.save()

        return redirect(
            'medical_records'
        )

    return render(
        request,
        'edit_medicalrecord.html',
        {'form': form}
    )
def delete_medical_record(request, id):

    record = MedicalRecord.objects.get(id=id)

    record.delete()

    return redirect(
        'medical_records'
    )



def prescription(request):

    # 👑 ADMIN
    if request.user.is_superuser or request.user.is_staff:
        prescriptions = Prescription.objects.all()

    # 👨‍⚕️ DOCTOR
    elif hasattr(request.user, 'doctor'):
        doctor = request.user.doctor
        prescriptions = Prescription.objects.filter(doctor=doctor)

    # 🧑‍🦰 PATIENT
    elif hasattr(request.user, 'patient'):
        patient = request.user.patient
        prescriptions = Prescription.objects.filter(patient=patient)

    else:
        return HttpResponse("Access Denied")

    return render(request, 'prescription.html', {
        'prescriptions': prescriptions
    })
   
def prescription_list(request):

    prescriptions = Prescription.objects.all()

    return render(
        request,
        'prescription_list.html',
        {'prescription': prescription}
    )
def add_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prescriptions')
    else:
        form = PrescriptionForm()

    return render(request, 'add_prescription.html', {'form': form})
def edit_prescription(request, id):

    prescription = Prescription.objects.get(
        id=id
    )

    form = PrescriptionForm(
        request.POST or None,
        instance=prescription
    )

    if form.is_valid():

        form.save()

        return redirect(
            'prescriptions'
        )

    return render(
        request,
        'edit_prescription.html',
        {'form': form}
    )
def delete_prescription(request, id):

    prescription = Prescription.objects.get(
        id=id
    )

    prescription.delete()

    return redirect(
        'prescriptions'
    )
from django.db.models import Q

def admin_dashboard(request):

    # Search
    query = request.GET.get('q', '')

    appointments = Appointment.objects.all().order_by('-appointment_date')

    if query:
        appointments = appointments.filter(
            Q(patient__name__icontains=query) |
            Q(doctor__name__icontains=query)
        )

    prescriptions = Prescription.objects.all()

    medical_records = MedicalRecord.objects.all()

    doctors = Doctor.objects.all()

    patients = Patient.objects.all()

    context = {

        # Counts
        'doctor_count': doctors.count(),

        'patient_count': patients.count(),

        'appointment_count': Appointment.objects.count(),

        'prescription_count': prescriptions.count(),

        'medical_count': medical_records.count(),

        # Data
        'appointments': appointments[:10],

        'prescriptions': prescriptions,

        'medical_records': medical_records,

        'doctors': doctors,

        'patients': patients,

        # Search
        'query': query,

    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )
def admin_profile(request):

    user = request.user

    if request.method == "POST":

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")

        user.save()

    return render(
        request,
        "admin_profile.html",
        {"user": user}
    )

def profile_settings(request):
    return render(request, 'profile_settings.html')

# Doctor Login


def doctor_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            try:
                Doctor.objects.get(user=user)

                login(request, user)

                return redirect("doctor_dashboard")

            except Doctor.DoesNotExist:

                messages.error(
                    request,
                    "You are not registered as a doctor."
                )

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "doctor_login.html"
    )

def patient_login(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user:

            login(request, user)

            return redirect("patient_dashboard")

        else:

            messages.error(request, "Invalid username or password.")

    return render(request, "patient_login.html")
  #admin login
def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")

    return render(request, "admin_login.html")


    return render(request, "patient_login.html")
def user_logout(request):
    logout(request)
    return redirect("home")



@login_required

def doctor_dashboard(request):

    doctor = Doctor.objects.get(user=request.user)

    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    appointments = Appointment.objects.filter(doctor=doctor)

    if query:
        appointments = appointments.filter(
            patient__name__icontains=query
        )

    if status_filter:
        appointments = appointments.filter(status=status_filter)

    patient_count = appointments.values('patient').distinct().count()

    medical_count = MedicalRecord.objects.filter(
        doctor=doctor
    ).count()

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'patient_count': patient_count,
        'appointment_count': appointments.count(),
        'medical_count': medical_count,
        'status_filter': status_filter,
    }

    return render(request, 'doctor_dashboard.html', context)
@login_required   



@login_required
def patient_dashboard(request):

    patient = get_object_or_404(Patient, user=request.user)

    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')
    records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')

    context = {
        'patient': patient,
        'appointment_count': appointments.count(),
        'prescription_count': prescriptions.count(),
        'medical_count': records.count(),
        'appointments': appointments[:5],
        'prescriptions': prescriptions[:5],
        'records': records[:5],
    }

    return render(request, 'patient_dashboard.html', context)
# Doctor Details
def doctor_detail(request, id):

    return render(
        request,
        'doctor_detail.html'
    )


# Department Details
def department_detail(request, id):

    return render(
        request,
        'department_detail.html'
    )