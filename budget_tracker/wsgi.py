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
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')

# Initialize Django
application = get_wsgi_application()

# Run migrations and create sample data automatically on Vercel
if os.environ.get('VERCEL'):
    try:
        # Import here to avoid circular imports
        from django.core.management import call_command
        from django.db import connection
        
        # Run migrations
        call_command('migrate', '--noinput', verbosity=0)
        
        # Create sample data for demo
        from expenses.models import Expense
        from decimal import Decimal
        
        # Check if we need to create sample data
        if not Expense.objects.exists():
            sample_data = [
                {
                    'description': 'Monthly Salary',
                    'amount': Decimal('50000.00'),
                    'category': 'salary',
                    'transaction_type': 'income'
                },
                {
                    'description': 'Grocery Shopping',
                    'amount': Decimal('2500.00'),
                    'category': 'food',
                    'transaction_type': 'expense'
                },
                {
                    'description': 'Transportation',
                    'amount': Decimal('1200.00'),
                    'category': 'transport',
                    'transaction_type': 'expense'
                },
                {
                    'description': 'Utilities Bill',
                    'amount': Decimal('3500.00'),
                    'category': 'bills',
                    'transaction_type': 'expense'
                }
            ]
            
            for data in sample_data:
                Expense.objects.create(**data)
                
    except Exception as e:
        print(f"Initialization error on Vercel: {e}")

# Vercel handler
app = application
