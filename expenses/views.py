from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .models import Expense
from .serializers import ExpenseSerializer

# API Views
class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class ExpenseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

@api_view(['GET'])
def expense_summary(request):
    """Get summary of income, expenses, and balance"""
    income_total = Expense.objects.filter(transaction_type='income').aggregate(
        total=Sum('amount'))['total'] or 0
    expense_total = Expense.objects.filter(transaction_type='expense').aggregate(
        total=Sum('amount'))['total'] or 0
    balance = income_total - expense_total
    
    return Response({
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance
    })

# Template Views
def dashboard(request):
    """Main dashboard view"""
    return render(request, 'expenses/dashboard.html')
