from django.db import models
from django.contrib.auth.models import User

class SocialMediaAccount(models.Model):
    PLATFORM_CHOICES = [
        ('FB', 'Facebook'),
        ('IG', 'Instagram'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES)
    account_id = models.CharField(max_length=255)
    access_token = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'platform', 'account_id']

class PostAnalytics(models.Model):
    account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=255)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    reach_count = models.IntegerField(default=0)
    engagement_rate = models.FloatField(default=0.0)
    posted_at = models.DateTimeField()
    analyzed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['account', 'post_id']

class EngagementMetrics(models.Model):
    account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)
    date = models.DateField()
    followers_count = models.IntegerField(default=0)
    profile_views = models.IntegerField(default=0)
    total_reach = models.IntegerField(default=0)
    total_impressions = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['account', 'date']

class AnalyticsReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title

class Metric(models.Model):
    report = models.ForeignKey(AnalyticsReport, on_delete=models.CASCADE, related_name='metrics')
    name = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.name}: {self.value}{self.unit}" 