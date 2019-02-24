from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

User = get_user_model()

class Lawyer(models.Model):
    user = models.OneToOneField(User, related_name="lawyer_user", on_delete=models.CASCADE)
    # The practise_number has letters and forward slashes e.g P.123/3456/89
    practise_number = models.CharField(max_length=15, primary_key=True)
    building_address = models.CharField(max_length=15)
    street_road = models.CharField(max_length=15)
    building_floor = models.CharField(max_length=15)
    status = models.BooleanField(default=False, help_text=(
            'Designates whether the user is available or not.'),)
    id_number = models.CharField(_('id_number'), max_length=15)
    phone_number = models.IntegerField(blank=True, null=True)


class Complainants(models.Model):
    OCCUPATION_CHOICES = (
        ('Uber Motorist', 'Uber Motorist'),
        ('Motor Cyclist', 'Motor Cyclist'),
    )
    user = models.OneToOneField(User, related_name="complainant_user", on_delete=models.CASCADE)
    occupation = models.CharField(
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default='Uber Motorist',
    )
    id_number = models.CharField(_('id_number'), max_length=15,)
    phone_number = models.IntegerField(blank=True, null=True)


class Offence(models.Model):
    fine = models.DecimalField(max_digits=6, decimal_places=0)
    creation_date = models.DateTimeField(_('date_created'),
                                         default=timezone.now)
    modification_date = models.DateTimeField(_('date_modified'),
                                             auto_now_add=True,
                                             blank=True, null=True)
    description = models.TextField(_('offence_description'))


class Complaint(models.Model):
    description = models.CharField(max_length=150)
    complainant = models.ForeignKey(Complainants, related_name='complainant', on_delete=models.CASCADE)
    location = models.CharField(max_length=40)
    status = models.BooleanField(default=False, help_text=(
            'Designates whether the complaint has been taken.'),)
    creation_date = models.DateTimeField(_('date_created'),
                                         default=timezone.now)
    modification_date = models.DateTimeField(_('date_modified'),
                                             auto_now_add=True,
                                             blank=True, null=True)

class Case(models.Model):
    lawyer = models.ForeignKey(Lawyer, related_name='case', on_delete=models.CASCADE)
    offence = models.ForeignKey(Offence, on_delete=models.SET_NULL, null=True, blank=True)
    status =  models.BooleanField(default=False)
    complaint = models.ForeignKey(Complaint, on_delete=models.SET_NULL, null=True, blank=True)
