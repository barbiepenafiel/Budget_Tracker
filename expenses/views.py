from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
import logging
import os
from .models import Expense
from .serializers import ExpenseSerializer

# Set up logging
logger = logging.getLogger(__name__)

# Health check endpoint
def health_check(request):
    """Simple health check endpoint"""
    try:
        # On Vercel, ensure database is initialized
        if os.environ.get('VERCEL'):
            from django.db import connection
            from django.core.management import call_command
            
            # Ensure database connection
            connection.ensure_connection()
            
            # Run migrations
            call_command('migrate', '--noinput', verbosity=0)
            
            # Create sample data if needed
            if not Expense.objects.exists():
                from decimal import Decimal
                sample_data = [
                    {
                        'description': 'Demo Income',
                        'amount': Decimal('25000.00'),
                        'category': 'salary',
                        'transaction_type': 'income'
                    },
                    {
                        'description': 'Demo Expense',
                        'amount': Decimal('1500.00'),
                        'category': 'food',
                        'transaction_type': 'expense'
                    }
                ]
                
                for data in sample_data:
                    Expense.objects.create(**data)
        
        return JsonResponse({
            'status': 'ok', 
            'message': 'Budget Tracker API is running!',
            'database_ready': True
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Database initialization failed: {str(e)}',
            'database_ready': False
        }, status=500)

# API Views
@method_decorator(csrf_exempt, name='dispatch')
class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            logger.info(f"Received POST data: {request.data}")
            
            # Ensure database is ready
            from django.db import connection
            from django.core.management import call_command
            
            # On Vercel, ensure migrations are run
            if os.environ.get('VERCEL'):
                try:
                    # Test database connection
                    connection.ensure_connection()
                    # Run migrations if needed
                    call_command('migrate', '--noinput', verbosity=0)
                except Exception as db_error:
                    logger.error(f"Database initialization error: {str(db_error)}")
            
            return super().post(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating expense: {str(e)}")
            return Response({
                'error': str(e),
                'detail': 'Failed to create expense'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
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
