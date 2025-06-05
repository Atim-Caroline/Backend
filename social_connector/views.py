from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import SocialAccount, SocialPost
from .serializers import SocialAccountSerializer, SocialPostSerializer
import requests
import json

class SocialAccountViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SocialAccountSerializer
    
    def get_queryset(self):
        return SocialAccount.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def refresh_token(self, request, pk=None):
        account = self.get_object()
        try:
            # Implement platform-specific token refresh logic
            if account.platform == 'twitter':
                # Twitter token refresh logic
                pass
            elif account.platform == 'linkedin':
                # LinkedIn token refresh logic
                pass
            elif account.platform == 'facebook':
                # Facebook token refresh logic
                pass
            
            return Response({'status': 'Token refreshed'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class SocialPostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SocialPostSerializer

    def get_queryset(self):
        return SocialPost.objects.filter(account__user=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        try:
            # Get the social account
            account = post.account
            
            # Get platform-specific API configuration
            api_config = settings.SOCIAL_API_CONFIGS.get(account.platform)
            
            if not api_config:
                raise ValueError(f"No API configuration found for {account.platform}")
            
            # Platform-specific posting logic
            if account.platform == 'twitter':
                # Twitter posting logic
                pass
            elif account.platform == 'linkedin':
                # LinkedIn posting logic
                pass
            elif account.platform == 'facebook':
                # Facebook posting logic
                pass
            
            post.status = 'published'
            post.save()
            
            return Response({'status': 'Post published successfully'})
        except Exception as e:
            post.status = 'failed'
            post.error_message = str(e)
            post.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        post = self.get_object()
        try:
            # Implement platform-specific analytics retrieval
            analytics_data = {
                'likes': 0,
                'shares': 0,
                'comments': 0,
                'reach': 0,
                'engagement_rate': 0.0
            }
            
            return Response(analytics_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def scheduled(self):
        posts = self.get_queryset().filter(status='scheduled')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def published(self):
        posts = self.get_queryset().filter(status='published')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data) 