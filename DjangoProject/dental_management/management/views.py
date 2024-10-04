from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Clinic, Doctor, Patient, Visit, Appointment, Procedure

def clinic_list(request):
    clinics = Clinic.objects.all()

    clinic_data = []
    for clinic in clinics:
        doctor_count = clinic.doctors.count()

        visit_count = Visit.objects.filter( clinic=clinic).count()
        appointment_count = Appointment.objects.filter( clinic=clinic).count()
        
        

        clinic_data.append({
            'clinic': clinic,
            'doctor_count': doctor_count,
            'patient_count': visit_count + appointment_count
        })

    return render(request, 'clinic_list.html', {'clinics': clinic_data})


def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    doctors = clinic.doctors.all()
    all_doctors = Doctor.objects.all()

    if request.method == 'POST':
        clinic.name = request.POST.get('name')
        clinic.phone_number = request.POST.get('phone_number')
        clinic.email = request.POST.get('email')
        clinic.city = request.POST.get('city')
        clinic.state = request.POST.get('state')
        clinic.save()

        selected_doctors = request.POST.getlist('doctors')
        clinic.doctors.set(selected_doctors)

        for doctor_id in selected_doctors:
            doctor = Doctor.objects.get(id=doctor_id)
            doctor.office_address = request.POST.get(f'office_address_{doctor.id}')
            doctor.working_schedule = request.POST.get(f'working_schedule_{doctor.id}')
            doctor.save()

        return redirect('clinic_detail', clinic_id=clinic.id)

    return render(request, 'clinic_detail.html', {
        'clinic': clinic,
        'doctors': doctors,
        'all_doctors': all_doctors
    })

def add_clinic(request):
    if request.method == 'POST':
        Clinic.objects.create(
            name=request.POST['name'],
            phone_number=request.POST['phone_number'],
            city=request.POST['city'],
            state=request.POST['state']
        )
        return redirect('clinic_list')
    return render(request, 'add_clinic.html')

def doctor_list(request):
    doctors = Doctor.objects.all()
    doctor_arr = []
    for doc in doctors:

        visit_count = Visit.objects.filter( doctor=doc).count()
        appointment_count = Appointment.objects.filter( doctor=doc).count()
        
        

        doctor_arr.append({
            'doctor': doc,
            'patient_count': visit_count + appointment_count
        })
    return render(request, 'doctor_list.html', {'doctors': doctor_arr})

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    SPECIALTY_CHOICES = [
        {'id': 'Cleaning', 'name': 'Cleaning'},
        {'id': 'Filling', 'name': 'Filling'},
        {'id': 'Root Canal', 'name': 'Root Canal'},
        {'id': 'Crown', 'name': 'Crown'},
        {'id': 'Teeth Whitening', 'name': 'Teeth Whitening'},
    ]

    clinics = doctor.clinics.all()
    visits = Visit.objects.filter(doctor=doctor)

    patients = Patient.objects.filter(visit__in=visits).distinct()

    if request.method == 'POST':
        doctor.npi = request.POST.get('npi')
        doctor.name = request.POST.get('name')
        doctor.email = request.POST.get('email')
        doctor.phone_number = request.POST.get('phone_number')
        doctor.specialties = request.POST.get('specialty')
        doctor.save()
        return redirect('doctor_detail', doctor_id=doctor.id)

    return render(request, 'doctor_detail.html', {
        'doctor': doctor, 
        'specialities': SPECIALTY_CHOICES,
        'clinics': clinics,
        'patients': patients
    })

def add_doctor(request):
    PROCEDURE_CHOICES = [
        {'id': 1, 'name': 'Cleaning'},
        {'id': 2, 'name': 'Filling'},
        {'id': 3, 'name': 'Root Canal'},
        {'id': 4, 'name': 'Crown'},
        {'id': 5, 'name': 'Teeth Whitening'},
    ]

    if request.method == 'POST':
        specialty_id = int(request.POST['specialty'])
        selected_specialty = next((specialty['name'] for specialty in PROCEDURE_CHOICES if specialty['id'] == specialty_id), None)

        Doctor.objects.create(
            npi=request.POST['npi'],
            name=request.POST['name'],
            email=request.POST['email'],
            specialties=selected_specialty
        )
        return redirect('doctor_list')
    
    return render(request, 'add_doctor.html', {'specialities': PROCEDURE_CHOICES})

def add_patient(request):
    if request.method == 'POST':
        Patient.objects.create(
            name=request.POST['name'],
            address=request.POST.get('address'),
            phone_number=request.POST.get('phone_number'),
            date_of_birth=request.POST['date_of_birth'],
            ssn=request.POST.get('ssn'),
            gender=request.POST.get('gender')
        )
        return redirect('patient_list')
    return render(request, 'add_patient.html')

def update_affiliations(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    
    if request.method == 'POST':
        selected_doctors = request.POST.getlist('doctors')
        clinic.doctors.set(selected_doctors)

        for doctor_id in selected_doctors:
            doctor = Doctor.objects.get(id=doctor_id)
            doctor.office_address = request.POST.get(f'office_address_{doctor.id}')
            doctor.working_schedule = request.POST.get(f'working_schedule_{doctor.id}')
            doctor.save()

    return redirect('clinic_detail', clinic_id=clinic.id)

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def patient_list(request):
    patients = Patient.objects.all()
    
    patient_visits = {}
    
    for patient in patients:
        last_visit = Visit.objects.filter(patient=patient).order_by('date').last()
        next_visit = Appointment.objects.filter(patient=patient).order_by('date').first()
        last_visit_doctor_name = last_visit.doctor.name if last_visit and last_visit.doctor else "N/A"
        next_visit_doctor_name = next_visit.doctor.name if next_visit and next_visit.doctor else "N/A"

        patient_visits[patient] = {
            'last_visit': last_visit,
            'next_visit': next_visit,
            'last_visit_doctor_name': last_visit_doctor_name,
            'next_visit_doctor_name': next_visit_doctor_name,
        }

    return render(request, 'patient_list.html', {'patient_visits': patient_visits})

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    print("pateint",patient.__dict__)
    visits = Visit.objects.filter(patient=patient)
    next_appointment = Appointment.objects.filter(patient=patient).order_by('date').first()

    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.address = request.POST.get('address')
        patient.phone_number = request.POST.get('phone_number')
        
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            patient.date_of_birth = date_of_birth
        else:
            patient.date_of_birth = None
        
        patient.ssn = request.POST.get('ssn')
        patient.gender = request.POST.get('gender')
        patient.save()
        return redirect('patient_detail', patient_id=patient.id)

    return render(request, 'patient_detail.html', {'patient': patient, 'visits': visits, 'next_appointment': next_appointment})

def add_visit(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        visit = Visit.objects.create(
            patient=patient,
            date=request.POST.get('date'),
            doctor_id=request.POST.get('doctor'),
            clinic_id=request.POST.get('clinic'),
            notes=request.POST.get('notes')
        )
        visit.procedures.set(request.POST.getlist('procedures'))
        visit.save()
        return redirect('patient_detail', patient_id=patient.id)
    
    doctors = Doctor.objects.all()
    clinics = Clinic.objects.all()
    procedures = Procedure.objects.all()

    return render(request, 'add_visit.html', {'patient': patient, 'doctors': doctors, 'clinics': clinics, 'procedures': procedures})

def schedule_appointment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    procedures = Procedure.objects.all()
    clinics = Clinic.objects.all()
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        appointment = Appointment.objects.create(
            patient=patient,
            date=request.POST.get('date'),
            doctor_id=request.POST.get('doctor'),
            clinic_id=request.POST.get('clinic'),
            procedure_id=request.POST.get('procedure')
        )
        return redirect('patient_detail', patient_id=patient.id)

    return render(request, 'schedule_appointment.html', {'patient': patient, 'procedures': procedures, 'clinics': clinics, 'doctors': doctors})

def get_available_time_slots(request):
    doctor_id = request.GET.get('doctor_id')
    clinic_id = request.GET.get('clinic_id')
    available_time_slots = ['09:00 AM', '10:00 AM', '11:00 AM']
    return JsonResponse({'time_slots': available_time_slots})

def get_procedures_by_doctor(request):
    doctor_id = request.GET.get('doctor_id')
    if doctor_id:
        doctor = Doctor.objects.get(id=doctor_id)
        procedures = Procedure.objects.filter(name=doctor.specialties)
        procedures_list = [{'id': procedure.id, 'name': procedure.name} for procedure in procedures]
        return JsonResponse(procedures_list, safe=False)
    return JsonResponse([], safe=False)

@login_required
def home(request):
    return render(request, 'home.html')

def custom_logout(request):
    logout(request)
    return redirect('login')