from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Expense(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSACTION_TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]
    
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('entertainment', 'Entertainment'),
        ('bills', 'Bills'),
        ('healthcare', 'Healthcare'),
        ('shopping', 'Shopping'),
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('investment', 'Investment'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    date_created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type.title()}: {self.description} - ₱{self.amount}"
