from django.contrib import admin
from django.urls import path, include
from devices.views import device_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('devices/', include('devices.urls')),
    path('', device_list_view, name='dashboard'),
]
