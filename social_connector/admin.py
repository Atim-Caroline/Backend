from django.contrib import admin
from .models import SocialAccount, SocialPost

@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'platform', 'account_name', 'is_active']
    list_filter = ['platform', 'is_active']
    search_fields = ['account_name', 'account_id']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ['account', 'content', 'scheduled_time', 'status']
    list_filter = ['status', 'account__platform']
    search_fields = ['content']
    readonly_fields = ['created_at', 'updated_at', 'post_id']
    ordering = ['-scheduled_time'] 