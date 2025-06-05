from rest_framework import serializers
from .models import ScheduledPost, PostReminder

class ScheduledPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledPost
        fields = ['id', 'title', 'content', 'image', 'scheduled_time', 'status', 'created_at', 'updated_at', 'published_post_id', 'error_message']
        read_only_fields = ['user', 'created_at', 'updated_at', 'published_post_id', 'error_message']

class PostReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReminder
        fields = ['id', 'title', 'description', 'frequency', 'preferred_time', 'is_active', 'created_at', 'last_reminded_at']
        read_only_fields = ['user', 'created_at', 'last_reminded_at'] 