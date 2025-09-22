from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    # Template views
    path('', views.dashboard, name='dashboard'),
    
    # API endpoints
    path('api/expenses/', views.ExpenseListCreateAPIView.as_view(), name='expense-list-create'),
    path('api/expenses/<int:pk>/', views.ExpenseRetrieveUpdateDestroyAPIView.as_view(), name='expense-detail'),
    path('api/summary/', views.expense_summary, name='expense-summary'),
]
