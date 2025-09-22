from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class UserLoginAttempt(models.Model):
    """Track user login attempts for account lockout functionality"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='login_attempts')
    failed_attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    locked_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Attempts: {self.failed_attempts}"

    def reset_attempts(self):
        """Reset failed attempts after successful login"""
        self.failed_attempts = 0
        self.is_locked = False
        self.locked_until = None
        self.save()

    def add_failed_attempt(self):
        """Add a failed attempt and lock if threshold reached"""
        self.failed_attempts += 1
        self.last_attempt = timezone.now()
        
        if self.failed_attempts >= getattr(settings, 'ACCOUNT_LOCKOUT_ATTEMPTS', 3):
            self.is_locked = True
            lockout_time = getattr(settings, 'ACCOUNT_LOCKOUT_TIME', 300)  # 5 minutes default
            self.locked_until = timezone.now() + timedelta(seconds=lockout_time)
        
        self.save()

    def is_account_locked(self):
        """Check if account is currently locked"""
        if not self.is_locked:
            return False
        
        if self.locked_until and timezone.now() > self.locked_until:
            # Unlock account if lockout time has passed
            self.is_locked = False
            self.locked_until = None
            self.failed_attempts = 0
            self.save()
            return False
        
        return self.is_locked

    def time_until_unlock(self):
        """Get remaining lockout time"""
        if not self.is_locked or not self.locked_until:
            return None
        
        remaining = self.locked_until - timezone.now()
        if remaining.total_seconds() <= 0:
            return None
        
        return remaining

class UserProfile(models.Model):
    """Extended user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_joined_formatted = models.DateTimeField(auto_now_add=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} Profile"
