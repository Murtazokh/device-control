from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Device, DeviceType, DeviceResponsibility
from .forms import DeviceFilterForm

@login_required
def device_list_view(request):
    user = request.user
    
    if user.role == 'ADMIN':
        devices = Device.objects.all()
    elif user.role == 'RESPONSIBLE':
        devices = Device.objects.filter(
            deviceresponsibility__responsible_person=user,
            deviceresponsibility__is_active=True
        ).distinct()
    elif user.role == 'TECHNICIAN':
        from services.models import ServiceRequest
        devices = Device.objects.filter(
            Q(servicerequest__assigned_technician=user) |
            Q(servicerequest__requested_by=user)
        ).distinct()
    else:
        devices = Device.objects.none()
    
    filter_form = DeviceFilterForm(request.GET)
    
    if filter_form.is_valid():
        device_type = filter_form.cleaned_data.get('device_type')
        status = filter_form.cleaned_data.get('status')
        branch = filter_form.cleaned_data.get('branch')
        department = filter_form.cleaned_data.get('department')
        search = filter_form.cleaned_data.get('search')
        
        if device_type:
            devices = devices.filter(device_type=device_type)
        if status:
            devices = devices.filter(status=status)
        if branch:
            devices = devices.filter(branch__icontains=branch)
        if department:
            devices = devices.filter(department__icontains=department)
        if search:
            devices = devices.filter(
                Q(name__icontains=search) |
                Q(serial_number__icontains=search) |
                Q(inventory_number__icontains=search) |
                Q(model__icontains=search)
            )
    
    devices = devices.select_related('device_type').prefetch_related(
        'deviceresponsibility_set__responsible_person',
        'deviceresponsibility_set__backup_person'
    )
    
    context = {
        'devices': devices,
        'filter_form': filter_form,
        'user_role': user.role,
        'total_devices': devices.count(),
    }
    
    return render(request, 'devices/device_list.html', context)

@login_required
def device_detail_view(request, pk):
    device = get_object_or_404(Device, pk=pk)
    user = request.user
    
    if user.role == 'ADMIN':
        pass
    elif user.role == 'RESPONSIBLE':
        if not DeviceResponsibility.objects.filter(
            device=device,
            responsible_person=user,
            is_active=True
        ).exists():
            messages.error(request, 'Sizda bu qurilmani ko\'rish huquqi yo\'q')
            return redirect('device_list')
    elif user.role == 'TECHNICIAN':
        from services.models import ServiceRequest
        if not ServiceRequest.objects.filter(
            Q(device=device) & 
            (Q(assigned_technician=user) | Q(requested_by=user))
        ).exists():
            messages.error(request, 'Sizda bu qurilmani ko\'rish huquqi yo\'q')
            return redirect('device_list')
    
    # Get responsible persons
    responsibilities = DeviceResponsibility.objects.filter(
        device=device,
        is_active=True
    ).select_related('responsible_person', 'backup_person')
    
    # Get service history
    from services.models import ServiceRequest
    service_requests = ServiceRequest.objects.filter(
        device=device
    ).select_related('requested_by', 'assigned_technician').order_by('-created_at')[:10]
    
    context = {
        'device': device,
        'responsibilities': responsibilities,
        'service_requests': service_requests,
        'user_role': user.role,
    }
    
    return render(request, 'devices/device_detail.html', context)