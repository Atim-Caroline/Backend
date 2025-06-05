from django.db import models
from django.contrib.auth.models import User
from analytics.models import SocialMediaAccount

class ScheduledPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Untitled Post")
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_post_id = models.CharField(max_length=255, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-scheduled_time']
        
    def __str__(self):
        return self.title

class PostAnalytics(models.Model):
    post = models.OneToOneField(ScheduledPost, on_delete=models.CASCADE, related_name='analytics')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    engagement_rate = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Analytics for {self.post.title}"

class PostReminder(models.Model):
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    preferred_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_reminded_at = models.DateTimeField(null=True, blank=True) 