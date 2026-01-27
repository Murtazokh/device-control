from django.db import models
from accounts.models import User
from devices.models import Device

class ServiceRequest(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Past'),
        ('MEDIUM', 'O\'rta'),
        ('HIGH', 'Yuqori'),
    ]
    
    STATUS_CHOICES = [
        ('NEW', 'Yangi'),
        ('ACCEPTED', 'Qabul qilindi'),
        ('IN_PROGRESS', 'Jarayonda'),
        ('COMPLETED', 'Bajarildi'),
        ('CANCELLED', 'Bekor qilindi'),
    ]
    
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name='service_requests'
    )
    assigned_technician = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='assigned_services'
    )
    
    problem_type = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class ServiceHistory(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    
    work_description = models.TextField()
    parts_replaced = models.TextField(blank=True)
    time_spent = models.DecimalField(max_digits=5, decimal_places=2)
    
    service_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)