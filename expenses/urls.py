from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health-check'),
    
    # Template views
    path('', views.dashboard, name='dashboard'),
    
    # API endpoints
    path('api/expenses/', views.ExpenseListCreateAPIView.as_view(), name='expense-list-create'),
    path('api/expenses/<int:pk>/', views.ExpenseRetrieveUpdateDestroyAPIView.as_view(), name='expense-detail'),
    path('api/summary/', views.expense_summary, name='expense-summary'),
    path('api/reset/', views.reset_data, name='reset-data'),
]
