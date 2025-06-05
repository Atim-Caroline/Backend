from rest_framework import serializers
from .models import ContentRule, ComplianceCheck, ComplianceReport

class ContentRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentRule
        fields = [
            'id', 'name', 'description', 'rule_type', 'pattern',
            'is_active', 'severity', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ComplianceCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceCheck
        fields = ['id', 'post', 'rule', 'status', 'details', 'checked_at']
        read_only_fields = ['checked_at']

class ComplianceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceReport
        fields = [
            'id', 'post', 'overall_status', 'failed_rules',
            'report_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at'] 