from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import UsernameValidator, ComplexPasswordValidator
from .models import UserLoginAttempt

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-white placeholder-gray-400',
            'placeholder': 'Enter your email'
        })
    )
    
    username = forms.CharField(
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-white placeholder-gray-400',
            'placeholder': 'Enter username (min 6 characters)'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-white placeholder-gray-400',
            'placeholder': 'Enter password (min 8 characters with special chars)'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-white placeholder-gray-400',
            'placeholder': 'Confirm your password'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        validator = UsernameValidator()
        validator.validate(username)
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        
        return username
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validator = ComplexPasswordValidator()
        validator.validate(password)
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create login attempt tracker
            UserLoginAttempt.objects.create(user=user)
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-white placeholder-gray-400',
            'placeholder': 'Enter your username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-white placeholder-gray-400',
            'placeholder': 'Enter your password'
        })
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username:
            try:
                user = User.objects.get(username=username)
                login_attempt, created = UserLoginAttempt.objects.get_or_create(user=user)
                
                if login_attempt.is_account_locked():
                    time_remaining = login_attempt.time_until_unlock()
                    if time_remaining:
                        minutes = int(time_remaining.total_seconds() // 60)
                        seconds = int(time_remaining.total_seconds() % 60)
                        raise ValidationError(
                            f"Account is locked due to too many failed attempts. "
                            f"Try again in {minutes}m {seconds}s."
                        )
            except User.DoesNotExist:
                pass
        
        return super().clean()
