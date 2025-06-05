from django.db import models
from django.contrib.auth.models import User

class SocialAccount(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('instagram', 'Instagram'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    account_id = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    access_token = models.CharField(max_length=512)
    refresh_token = models.CharField(max_length=512, blank=True, null=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'platform', 'account_id']
        
    def __str__(self):
        return f"{self.account_name} ({self.platform})"

class SocialPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    ]
    
    account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    content = models.TextField()
    media_url = models.URLField(max_length=512, blank=True, null=True)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    post_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_time']
        
    def __str__(self):
        return f"{self.content[:50]}... ({self.status})" 