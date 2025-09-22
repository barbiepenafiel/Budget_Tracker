"""
Production settings for Vercel deployment
"""
import os
from .settings import *

# Override settings for production
DEBUG = False
ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files for production
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Database configuration for production (using SQLite for simplicity)
# In a real production environment, you'd want to use PostgreSQL or MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
