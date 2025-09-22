#!/usr/bin/env python
"""
Management script for database initialization on Vercel
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create sample data if database is empty
    from expenses.models import Expense
    if not Expense.objects.exists():
        execute_from_command_line(['manage.py', 'create_sample_data'])
