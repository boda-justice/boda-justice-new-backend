from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Offence)
admin.site.register(models.Lawyer)
admin.site.register(models.Complainants)
admin.site.register(models.Case)
admin.site.register(models.Complaint)
admin.site.register(models.PoliceStation)
admin.site.register(models.Reviews)
