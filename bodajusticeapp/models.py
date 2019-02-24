from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The practise_number has letters and forward slashes e.g P.123/3456/89
    practise_number = models.CharField(max_length=15, primary_key=True)
    building_address = models.CharField(max_length=15)
    street_road = models.CharField(max_length=15)
    building_floor = models.CharField(max_length=15)
    status = models.BooleanField(default=False, help_text=(
            'Designates whether the user is available or not.'),)


class Complainants(models.Model):
    OCCUPATION_CHOICES = (
        ('Uber Motorist', 'Uber Motorist'),
        ('Motor Cyclist', 'Motor Cyclist'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default='Uber Motorist',
    )


class Offence(models.Model):
    description = models.CharField(max_length=200)
    offense_type = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    fine = models.IntegerField()


class Complaint(models.Model):
    description = models.CharField(max_length=150)
    complainant = models.ForeignKey(Complainants, related_name='complainant', on_delete=models.CASCADE)
    location = models.CharField(max_length=40)

class Case(models.Model):
    lawyer = models.ForeignKey(User, related_name='case', on_delete=models.CASCADE)
    offence = models.CharField(max_length=50),
    status = models.BooleanField(default=False)
    # complaint = models.ForeignKey()
