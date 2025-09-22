from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserLoginAttempt, UserProfile

@admin.register(UserLoginAttempt)
class UserLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'failed_attempts', 'is_locked', 'last_attempt', 'locked_until']
    list_filter = ['is_locked', 'last_attempt']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['user']
        return self.readonly_fields

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_joined_formatted', 'last_login_ip', 'is_email_verified']
    list_filter = ['is_email_verified', 'date_joined_formatted']
    search_fields = ['user__username', 'user__email']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ['user', 'date_joined_formatted']
        return ['date_joined_formatted']

# Customize the default User admin to show login attempts
class UserLoginAttemptInline(admin.StackedInline):
    model = UserLoginAttempt
    extra = 0
    readonly_fields = ['failed_attempts', 'last_attempt', 'is_locked', 'locked_until', 'created_at', 'updated_at']

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    readonly_fields = ['date_joined_formatted']

class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline, UserLoginAttemptInline]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
