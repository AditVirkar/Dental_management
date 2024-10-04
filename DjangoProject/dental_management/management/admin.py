from django.contrib import admin

from .models import Clinic, Doctor, Patient,Procedure, Visit, Appointment

admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Procedure)
admin.site.register(Visit)
admin.site.register(Appointment)