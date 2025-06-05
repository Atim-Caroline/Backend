from django.db import models
from django.contrib.auth.models import User

class TrendingTopic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    volume = models.IntegerField(default=0)
    sentiment = models.FloatField(default=0.0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-volume']
        
    def __str__(self):
        return self.name

class TrendInsight(models.Model):
    topic = models.ForeignKey(TrendingTopic, on_delete=models.CASCADE, related_name='insights')
    title = models.CharField(max_length=200)
    content = models.TextField()
    source = models.CharField(max_length=200)
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return self.title

class UserTrendAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keywords = models.TextField(help_text='Comma-separated keywords to track')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_notified = models.DateTimeField(null=True, blank=True)
    min_volume = models.IntegerField(default=0)
    platforms = models.CharField(max_length=50, help_text='Comma-separated platforms to track')

class TrendNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trend = models.ForeignKey(TrendingTopic, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_text = models.TextField()

    class Meta:
        ordering = ['-created_at'] 