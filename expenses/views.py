from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from django.views.decorators.http import require_http_methods
from django.conf import settings
import logging
import os
from .models import Expense
from .serializers import ExpenseSerializer

# Set up logging
logger = logging.getLogger(__name__)

def vercel_csrf_exempt(view_func):
    """
    Decorator to exempt CSRF checking in Vercel environment
    """
    def wrapper(request, *args, **kwargs):
        # Check if we're in Vercel environment
        if os.environ.get('VERCEL') or settings.DEBUG:
            # Skip CSRF for Vercel or debug mode
            return csrf_exempt(view_func)(request, *args, **kwargs)
        else:
            # Apply normal CSRF protection in production
            return view_func(request, *args, **kwargs)
    return wrapper

# Health check endpoint (no auth required)
def health_check(request):
    """Simple health check endpoint"""
    try:
        # Test database connection
        expense_count = Expense.objects.count()
        user_count = 0
        
        # Try to get user count if authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_count = Expense.objects.filter(user=request.user).count()
        
        return JsonResponse({
            'status': 'ok', 
            'message': 'Budget Tracker API is running!',
            'database_ready': True,
            'total_expenses_in_system': expense_count,
            'user_expenses': user_count,
            'vercel_environment': bool(os.environ.get('VERCEL')),
            'debug_mode': getattr(settings, 'DEBUG', False)
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

@vercel_csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_data(request):
    """Reset all expense data for current user - for new user experience"""
    try:
        user = request.user
        username = user.username
        
        # Log the attempt with more detail
        logger.info(f"User {username} (id: {user.id}) attempting to reset their data")
        
        # Check if user is properly authenticated
        if not user.is_authenticated:
            logger.error(f"Unauthenticated user attempting to reset data")
            return Response({
                'status': 'error',
                'message': 'Authentication required',
                'error_type': 'authentication'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Delete all expenses for current user only - use a more robust approach
        deleted_count = 0
        try:
            # First count to verify we have access
            expense_count = Expense.objects.filter(user=user).count()
            logger.info(f"User {username} has {expense_count} expenses to delete")
            
            # Then delete
            if expense_count > 0:
                deleted_result = Expense.objects.filter(user=user).delete()
                deleted_count = deleted_result[0] if deleted_result else 0
            
            logger.info(f"User {username} reset their data. {deleted_count} transactions deleted.")
        except Exception as db_error:
            logger.error(f"Database error while resetting data for {username}: {str(db_error)}")
            return Response({
                'status': 'error',
                'message': f'Database error: {str(db_error)}',
                'error_type': 'database'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Force session save to ensure Vercel persistence
        try:
            request.session['last_reset'] = username
            request.session['reset_timestamp'] = str(timezone.now())
            request.session.modified = True
            request.session.save()
        except Exception as session_error:
            logger.warning(f"Session error for {username}, but data was reset: {str(session_error)}")
            # Don't return error here, as the main operation succeeded
        
        # Return success response
        return Response({
            'status': 'success',
            'message': f'All your data reset successfully. {deleted_count} transactions deleted.',
            'clear_local_storage': True,
            'username': username,  # Include username for client-side localStorage clearing
            'deleted_count': deleted_count,
            'timestamp': str(timezone.now())
        })
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Unexpected error resetting data for user {getattr(request.user, 'username', 'unknown')}: {error_msg}")
        
        # Return a more detailed error response
        return Response({
            'status': 'error',
            'message': f'Failed to reset data: {error_msg}',
            'error_type': 'unexpected',
            'username': getattr(request.user, 'username', 'unknown')
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Template Views (Authenticated)
@login_required
def dashboard(request):
    """Main dashboard view - requires authentication"""
    return render(request, 'expenses/dashboard.html', {
        'user': request.user
    })
