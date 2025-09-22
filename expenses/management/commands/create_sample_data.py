from django.core.management.base import BaseCommand
from expenses.models import Expense
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create sample expense data'

    def handle(self, *args, **options):
        # Sample data
        sample_expenses = [
            {
                'amount': Decimal('2500.00'),
                'description': 'Grocery shopping',
                'category': 'food',
                'transaction_type': 'expense'
            },
            {
                'amount': Decimal('125000.00'),
                'description': 'Monthly salary',
                'category': 'salary',
                'transaction_type': 'income'
            },
            {
                'amount': Decimal('1250.00'),
                'description': 'Gas for car',
                'category': 'transport',
                'transaction_type': 'expense'
            },
            {
                'amount': Decimal('1500.00'),
                'description': 'Movie tickets',
                'category': 'entertainment',
                'transaction_type': 'expense'
            },
            {
                'amount': Decimal('25000.00'),
                'description': 'Freelance project',
                'category': 'freelance',
                'transaction_type': 'income'
            },
            {
                'amount': Decimal('6000.00'),
                'description': 'Electricity bill',
                'category': 'bills',
                'transaction_type': 'expense'
            },
        ]

        for expense_data in sample_expenses:
            expense, created = Expense.objects.get_or_create(
                description=expense_data['description'],
                defaults=expense_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created expense: {expense.description}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Expense already exists: {expense.description}')
                )
