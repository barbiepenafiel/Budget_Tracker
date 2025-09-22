from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'category', 'transaction_type', 'date_created']
    list_filter = ['transaction_type', 'category', 'date_created']
    search_fields = ['description']
    ordering = ['-date_created']
