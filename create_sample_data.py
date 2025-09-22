import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')
django.setup()

from expenses.models import Expense

# Create sample data
sample_expenses = [
    {
        'title': 'Monthly Salary',
        'amount': Decimal('25000.00'),  # ₱25,000
        'category': 'salary',
        'transaction_type': 'income',
        'description': 'Monthly salary payment'
    },
    {
        'title': 'Grocery Shopping',
        'amount': Decimal('3500.00'),  # ₱3,500
        'category': 'food',
        'transaction_type': 'expense',
        'description': 'Weekly grocery shopping at SM'
    },
    {
        'title': 'Electric Bill',
        'amount': Decimal('2800.00'),  # ₱2,800
        'category': 'bills',
        'transaction_type': 'expense',
        'description': 'Monthly electric bill from Meralco'
    },
    {
        'title': 'Coffee Shop',
        'amount': Decimal('180.00'),  # ₱180
        'category': 'food',
        'transaction_type': 'expense',
        'description': 'Morning coffee and pastry at Starbucks'
    },
    {
        'title': 'Freelance Project',
        'amount': Decimal('15000.00'),  # ₱15,000
        'category': 'business',
        'transaction_type': 'income',
        'description': 'Web development freelance project'
    },
    {
        'title': 'Netflix Subscription',
        'amount': Decimal('549.00'),  # ₱549
        'category': 'entertainment',
        'transaction_type': 'expense',
        'description': 'Monthly Netflix subscription'
    },
    {
        'title': 'Grab Ride',
        'amount': Decimal('350.00'),  # ₱350
        'category': 'transportation',
        'transaction_type': 'expense',
        'description': 'Grab ride to Makati'
    },
    {
        'title': 'Investment Dividend',
        'amount': Decimal('2500.00'),  # ₱2,500
        'category': 'investment',
        'transaction_type': 'income',
        'description': 'Quarterly dividend from BDO stock'
    }
]

# Clear existing data
Expense.objects.all().delete()

# Create sample expenses
for expense_data in sample_expenses:
    Expense.objects.create(**expense_data)

print(f"Created {len(sample_expenses)} sample transactions!")
print("Sample data includes both income and expenses across different categories.")
