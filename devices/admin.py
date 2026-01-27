from django.contrib import admin
from devices.models import Device, DeviceType, DeviceResponsibility

admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(DeviceResponsibility)