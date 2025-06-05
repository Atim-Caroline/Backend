from rest_framework import serializers
from .models import SocialAccount, SocialPost

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ['id', 'platform', 'account_id', 'account_name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class SocialPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialPost
        fields = ['id', 'account', 'content', 'media_url', 'scheduled_time', 'status', 'post_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'post_id'] 