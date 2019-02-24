from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Offence)
admin.site.register(models.Lawyer)
admin.site.register(models.Complainants)