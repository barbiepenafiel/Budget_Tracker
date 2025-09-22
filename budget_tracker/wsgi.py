"""
WSGI config for budget_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')

# Initialize Django
application = get_wsgi_application()

# Initialize database only once on Vercel
if os.environ.get('VERCEL'):
    import threading
    _init_lock = threading.Lock()
    _initialized = False
    
    def init_database():
        global _initialized
        if _initialized:
            return
            
        with _init_lock:
            if _initialized:
                return
                
            try:
                from django.core.management import call_command
                from django.db import connection
                import sqlite3
                
                # Check if database file exists and has tables
                db_path = '/tmp/db.sqlite3'
                needs_setup = True
                
                if os.path.exists(db_path):
                    try:
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses_expense';")
                        if cursor.fetchone():
                            needs_setup = False
                        conn.close()
                    except:
                        needs_setup = True
                
                if needs_setup:
                    # Run migrations
                    call_command('migrate', '--noinput', verbosity=0)
                    
                    # Create a superuser for admin access (only if none exists)
                    from django.contrib.auth.models import User
                    if not User.objects.filter(is_superuser=True).exists():
                        try:
                            User.objects.create_superuser(
                                username='admin',
                                email='admin@example.com',
                                password='admin123!@#'
                            )
                            print("Superuser 'admin' created for testing")
                        except Exception as e:
                            print(f"Could not create superuser: {e}")
                    
                    print("Database initialized with clean state and authentication")
                
                _initialized = True
                
            except Exception as e:
                print(f"Database initialization error: {e}")
    
    # Initialize on first import
    init_database()

# Vercel handler
app = application
