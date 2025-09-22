from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
import logging
import os
from .models import Expense
from .serializers import ExpenseSerializer

# Set up logging
logger = logging.getLogger(__name__)

# Health check endpoint (no auth required)
def health_check(request):
    """Simple health check endpoint"""
    try:
        # Test database connection
        expense_count = Expense.objects.count()
        return JsonResponse({
            'status': 'ok', 
            'message': 'Budget Tracker API is running!',
            'database_ready': True,
            'total_expenses_in_system': expense_count
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Database error: {str(e)}',
            'database_ready': False
        }, status=500)

# API Views (Authenticated)
@method_decorator(csrf_exempt, name='dispatch')
class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return expenses for the current user only"""
        return Expense.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Save the expense with the current user"""
        serializer.save(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        try:
            logger.info(f"User {request.user.username} creating expense: {request.data}")
            return super().post(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating expense for user {request.user.username}: {str(e)}")
            return Response({
                'error': str(e),
                'detail': 'Failed to create expense'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class ExpenseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return expenses for the current user only"""
        return Expense.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_summary(request):
    """Get summary of income, expenses, and balance for current user"""
    user_expenses = Expense.objects.filter(user=request.user)
    
    income_total = user_expenses.filter(transaction_type='income').aggregate(
        total=Sum('amount'))['total'] or 0
    expense_total = user_expenses.filter(transaction_type='expense').aggregate(
        total=Sum('amount'))['total'] or 0
    balance = income_total - expense_total
    
    return Response({
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance,
        'user': request.user.username
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_data(request):
    """Reset all expense data for current user - for new user experience"""
    try:
        # Delete all expenses for current user only
        deleted_count = Expense.objects.filter(user=request.user).delete()[0]
        
        logger.info(f"User {request.user.username} reset their data. {deleted_count} transactions deleted.")
        
        return Response({
            'status': 'success',
            'message': f'All your data reset successfully. {deleted_count} transactions deleted.',
            'clear_local_storage': True
        })
    except Exception as e:
        logger.error(f"Error resetting data for user {request.user.username}: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Failed to reset data: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Template Views (Authenticated)
@login_required
def dashboard(request):
    """Main dashboard view - requires authentication"""
    return render(request, 'expenses/dashboard.html', {
        'user': request.user
    })
