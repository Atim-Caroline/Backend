from django.contrib import admin
from .models import ContentRule, ComplianceCheck, ComplianceReport

@admin.register(ContentRule)
class ContentRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'rule_type', 'is_active', 'severity', 'created_at']
    list_filter = ['rule_type', 'is_active', 'severity']
    search_fields = ['name', 'description', 'pattern']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ComplianceCheck)
class ComplianceCheckAdmin(admin.ModelAdmin):
    list_display = ['post', 'rule', 'status', 'checked_at']
    list_filter = ['status', 'rule__rule_type']
    search_fields = ['post__content', 'rule__name']
    readonly_fields = ['checked_at']

@admin.register(ComplianceReport)
class ComplianceReportAdmin(admin.ModelAdmin):
    list_display = ['post', 'overall_status', 'created_at']
    list_filter = ['overall_status']
    search_fields = ['post__content']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['failed_rules'] 