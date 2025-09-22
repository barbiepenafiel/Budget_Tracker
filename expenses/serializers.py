from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'category', 'transaction_type', 'date_created']
        read_only_fields = ['id', 'date_created']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
