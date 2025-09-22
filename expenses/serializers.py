from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'category', 'transaction_type', 'date_created', 'username']
        read_only_fields = ['id', 'date_created', 'username']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def get_username(self, obj):
        """Include username to help with cross-device localStorage handling"""
        return obj.user.username if obj.user else None
