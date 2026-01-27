from django.contrib import admin
from services.models import ServiceRequest, ServiceHistory

admin.site.register(ServiceRequest)
admin.site.register(ServiceHistory)