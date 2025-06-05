from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SocialPost
from compliance_service.models import ComplianceCheck, ContentRule, ComplianceReport

@receiver(post_save, sender=SocialPost)
def trigger_compliance_check(sender, instance, created, **kwargs):
    if created or instance.content_changed():
        # Get all active rules
        active_rules = ContentRule.objects.filter(is_active=True)
        
        # Create compliance checks for each rule
        checks = []
        for rule in active_rules:
            check = ComplianceCheck.objects.create(
                post=instance,
                rule=rule,
                status='pending'
            )
            checks.append(check)
        
        # Create a compliance report
        ComplianceReport.objects.create(
            post=instance,
            overall_status='pending',
            report_data={
                'total_rules': len(checks),
                'pending_checks': len(checks),
                'passed_checks': 0,
                'failed_checks': 0
            }
        ) 