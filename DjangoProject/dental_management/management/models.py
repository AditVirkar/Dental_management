from django.db import models

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Procedure(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    SPECIALTY_CHOICES = [
        ('Cleaning', 'Cleaning'),
        ('Filling', 'Filling'),
        ('Root Canal', 'Root Canal'),
        ('Crown', 'Crown'),
        ('Teeth Whitening', 'Teeth Whitening'),
    ]

    npi = models.CharField(max_length=10, unique=True, default='0000000000')
    name = models.CharField(max_length=100, default='Dane Jone')
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, default='123-456-7890')
    specialties = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, default='Teeth Whitening')
    office_address = models.CharField(max_length=255, blank=True, null=True)
    working_schedule = models.CharField(max_length=255, blank=True, null=True)
    clinics = models.ManyToManyField(Clinic, related_name='doctors', blank=True)

    def __str__(self):
        return self.name

    def clinic_count(self):
        return self.clinics.count()

    def patient_count(self):
        return self.last_visit_patients.count() + self.next_appointment_patients.count()

class Visit(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True)
    procedures = models.ManyToManyField(Procedure)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.name} - {self.date}"

class Appointment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True)
    procedure = models.ForeignKey(Procedure, on_delete=models.SET_NULL, null=True)
    date_booked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.date} with {self.doctor.name}"

class Patient(models.Model):
    name = models.CharField(max_length=100, default='Unknown')
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    ssn = models.CharField(max_length=4, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Unknown')

    last_visit_date = models.DateField(null=True, blank=True)
    last_visit_doctor = models.ForeignKey(Doctor, null=True, blank=True, related_name='last_visit_patients', on_delete=models.SET_NULL)
    last_visit_procedures = models.ManyToManyField(Procedure, blank=True, related_name='last_visit_procedures')

    next_appointment_date = models.DateField(null=True, blank=True)
    next_appointment_doctor = models.ForeignKey(Doctor, null=True, blank=True, related_name='next_appointment_patients', on_delete=models.SET_NULL)
    next_appointment_procedure = models.ManyToManyField(Procedure, blank=True, related_name='next_appointment_procedures')

    def __str__(self):
        return self.name
