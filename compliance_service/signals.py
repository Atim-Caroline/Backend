from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from .models import ComplianceCheck, ComplianceReport

@receiver(post_save, sender=ComplianceCheck)
def update_compliance_report(sender, instance, **kwargs):
    # Get or create the compliance report for this post
    report, created = ComplianceReport.objects.get_or_create(
        post=instance.post,
        defaults={
            'overall_status': 'pending',
            'report_data': {
                'total_rules': 0,
                'pending_checks': 0,
                'passed_checks': 0,
                'failed_checks': 0
            }
        }
    )

    # Get aggregated check statuses
    check_stats = ComplianceCheck.objects.filter(
        post=instance.post
    ).values('status').annotate(count=Count('id'))

    # Convert to a more usable format
    stats = {
        'total_rules': sum(stat['count'] for stat in check_stats),
        'pending_checks': 0,
        'passed_checks': 0,
        'failed_checks': 0
    }

    for stat in check_stats:
        if stat['status'] == 'pending':
            stats['pending_checks'] = stat['count']
        elif stat['status'] == 'passed':
            stats['passed_checks'] = stat['count']
        elif stat['status'] == 'failed':
            stats['failed_checks'] = stat['count']

    # Update the report status
    if stats['pending_checks'] > 0:
        overall_status = 'pending'
    elif stats['failed_checks'] > 0:
        overall_status = 'failed'
    else:
        overall_status = 'passed'

    # Update the report
    report.overall_status = overall_status
    report.report_data = stats
    
    # If any checks failed, add them to failed_rules
    if instance.status == 'failed':
        report.failed_rules.add(instance.rule)
    elif instance.status == 'passed':
        report.failed_rules.remove(instance.rule)
    
    report.save() 