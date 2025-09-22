import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')
django.setup()

from django.contrib.auth.models import User

# Set password for admin user
admin_user = User.objects.get(username='admin')
admin_user.set_password('admin123')
admin_user.save()

print("Admin password set to 'admin123'")
