from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('RESPONSIBLE', 'Javobgar Shaxs'),
        ('TECHNICIAN', 'Servis Xodimi'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_on_vacation = models.BooleanField(default=False)
    is_active_employee = models.BooleanField(default=True)