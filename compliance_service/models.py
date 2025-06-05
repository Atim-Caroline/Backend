from django.db import models
from social_connector.models import SocialPost

class ContentRule(models.Model):
    RULE_TYPE_CHOICES = [
        ('keyword', 'Keyword Filter'),
        ('regex', 'Regular Expression'),
        ('sentiment', 'Sentiment Analysis'),
        ('profanity', 'Profanity Check'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    pattern = models.TextField()
    is_active = models.BooleanField(default=True)
    severity = models.IntegerField(default=1)  # 1: Low, 2: Medium, 3: High
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.rule_type}"

class ComplianceCheck(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]

    post = models.ForeignKey(SocialPost, on_delete=models.CASCADE)
    rule = models.ForeignKey(ContentRule, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    details = models.JSONField(null=True, blank=True)
    checked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Check for {self.post} against {self.rule}"

class ComplianceReport(models.Model):
    post = models.ForeignKey(SocialPost, on_delete=models.CASCADE)
    overall_status = models.CharField(max_length=20)
    failed_rules = models.ManyToManyField(ContentRule)
    report_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Compliance Report for {self.post} - {self.overall_status}" 