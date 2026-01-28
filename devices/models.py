from django.db import models
from accounts.models import User

class DeviceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    STATUS_CHOICES = [
        ('WORKING', 'Ishlayapti'),
        ('BROKEN', 'Nosoz'),
        ('IN_SERVICE', 'Servisda'),
        ('DECOMMISSIONED', 'Hisobdan chiqarilgan'),
    ]
    
    name = models.CharField(max_length=200)
    device_type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    inventory_number = models.CharField(max_length=100, unique=True)
    
    # Location
    branch = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    room = models.CharField(max_length=50, blank=True)
    
    manufacturer = models.CharField(max_length=100)
    installation_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    operating_system = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DeviceResponsibility(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    responsible_person = models.ForeignKey(User, on_delete=models.CASCADE)
    backup_person = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='backup_devices'
    )
    assigned_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.device.name} - {self.responsible_person.username}"
