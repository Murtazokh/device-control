from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomLoginForm, CustomUserCreationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Xush kelibsiz, {user.username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Username yoki parol noto\'g\'ri')
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Tizimdan chiqdingiz')
    return redirect('login')

@login_required
def dashboard_view(request):
    user = request.user
    
    if user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif user.role == 'RESPONSIBLE':
        return redirect('responsible_dashboard')
    elif user.role == 'TECHNICIAN':
        return redirect('technician_dashboard')
    else:
        return render(request, 'base.html')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})