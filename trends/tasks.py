from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import TrendingTopic, UserTrendAlert, TrendNotification
import facebook
import requests
from textblob import TextBlob

@shared_task
def fetch_trending_topics():
    # Facebook Graph API trending topics (requires appropriate permissions)
    accounts = SocialMediaAccount.objects.filter(platform='FB')
    
    for account in accounts:
        try:
            graph = facebook.GraphAPI(access_token=account.access_token)
            
            # Get trending topics from Facebook
            trending = graph.get_connections('me', 'trending')
            
            for topic in trending['data']:
                # Calculate sentiment using TextBlob
                analysis = TextBlob(topic.get('description', ''))
                sentiment_score = analysis.sentiment.polarity
                
                TrendingTopic.objects.create(
                    topic=topic['name'],
                    platform='FB',
                    volume=topic.get('volume', 0),
                    sentiment_score=sentiment_score,
                    region=topic.get('region', 'Global')
                )
                
        except Exception as e:
            print(f"Error fetching Facebook trends: {str(e)}")
    
    # Instagram trending hashtags (requires Instagram Graph API business account)
    accounts = SocialMediaAccount.objects.filter(platform='IG')
    
    for account in accounts:
        try:
            base_url = 'https://graph.instagram.com/v12.0'
            
            # Get trending hashtags
            response = requests.get(
                f"{base_url}/ig_hashtag_search",
                params={
                    'access_token': account.access_token,
                    'q': ''  # Empty query to get trending hashtags
                }
            )
            
            if response.status_code == 200:
                hashtags = response.json()['data']
                
                for hashtag in hashtags:
                    # Get hashtag info
                    info_response = requests.get(
                        f"{base_url}/{hashtag['id']}",
                        params={
                            'access_token': account.access_token,
                            'fields': 'name,media_count'
                        }
                    )
                    
                    if info_response.status_code == 200:
                        hashtag_info = info_response.json()
                        
                        TrendingTopic.objects.create(
                            topic=hashtag_info['name'],
                            platform='IG',
                            volume=hashtag_info.get('media_count', 0),
                            sentiment_score=0.0,  # Instagram API doesn't provide sentiment data
                            region='Global'
                        )
                        
        except Exception as e:
            print(f"Error fetching Instagram trends: {str(e)}")

@shared_task
def process_trend_alerts():
    alerts = UserTrendAlert.objects.filter(is_active=True)
    
    for alert in alerts:
        try:
            keywords = [k.strip() for k in alert.keywords.split(',')]
            platforms = [p.strip() for p in alert.platforms.split(',')]
            
            # Get trending topics that match the user's criteria
            matching_trends = TrendingTopic.objects.filter(
                platform__in=platforms,
                volume__gte=alert.min_volume,
                created_at__gte=timezone.now() - timezone.timedelta(hours=24)
            ).filter(topic__in=keywords)
            
            for trend in matching_trends:
                # Create notification
                notification = TrendNotification.objects.create(
                    user=alert.user,
                    trend=trend,
                    notification_text=f"Trending on {trend.get_platform_display()}: {trend.topic} "
                                    f"(Volume: {trend.volume})"
                )
                
                # Send email notification
                send_mail(
                    subject=f"Trending Alert: {trend.topic}",
                    message=f"""
                    Hello {alert.user.username},
                    
                    We detected a trending topic that matches your alert criteria:
                    
                    Topic: {trend.topic}
                    Platform: {trend.get_platform_display()}
                    Volume: {trend.volume}
                    Sentiment: {'Positive' if trend.sentiment_score > 0 else 'Negative' if trend.sentiment_score < 0 else 'Neutral'}
                    
                    Best regards,
                    Your Social Media Assistant
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[alert.user.email],
                )
                
            alert.last_notified = timezone.now()
            alert.save()
            
        except Exception as e:
            print(f"Error processing trend alert {alert.id}: {str(e)}")

@shared_task
def cleanup_old_trends():
    # Remove trends older than 7 days
    cutoff_date = timezone.now() - timezone.timedelta(days=7)
    TrendingTopic.objects.filter(created_at__lt=cutoff_date).delete() 