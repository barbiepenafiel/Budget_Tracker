from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import UserLoginAttempt

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_protect
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('expenses:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('authentication:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'authentication/register.html', {'form': form})

@csrf_protect
def login_view(request):
    """User login view with account lockout"""
    if request.user.is_authenticated:
        return redirect('expenses:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Reset login attempts on successful login
                try:
                    login_attempt = UserLoginAttempt.objects.get(user=user)
                    login_attempt.reset_attempts()
                except UserLoginAttempt.DoesNotExist:
                    UserLoginAttempt.objects.create(user=user)
                
                # Update last login IP
                if hasattr(user, 'profile'):
                    user.profile.last_login_ip = get_client_ip(request)
                    user.profile.save()
                
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('expenses:dashboard')
        else:
            # Handle failed login attempt
            username = request.POST.get('username')
            if username:
                try:
                    user = UserLoginAttempt.objects.select_related('user').get(user__username=username).user
                    login_attempt, created = UserLoginAttempt.objects.get_or_create(user=user)
                    login_attempt.add_failed_attempt()
                    
                    remaining_attempts = 3 - login_attempt.failed_attempts
                    if remaining_attempts > 0:
                        messages.error(request, f'Invalid credentials. {remaining_attempts} attempts remaining.')
                    else:
                        messages.error(request, 'Account locked due to too many failed attempts.')
                except:
                    messages.error(request, 'Invalid credentials.')
            else:
                messages.error(request, 'Please enter valid credentials.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def logout_view(request):
    """User logout view"""
    username = request.user.username
    logout(request)
    messages.success(request, f'Goodbye, {username}! You have been logged out successfully.')
    return redirect('authentication:login')

@method_decorator(csrf_protect, name='dispatch')
class RegisterView(CreateView):
    """Class-based registration view"""
    form_class = CustomUserCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('authentication:login')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('expenses:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Registration successful! You can now log in.')
        return super().form_valid(form)
