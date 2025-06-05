from celery import shared_task
from datetime import datetime, timedelta
from .models import SocialMediaAccount, PostAnalytics, EngagementMetrics
import facebook
import requests

@shared_task
def fetch_facebook_insights(account_id):
    try:
        account = SocialMediaAccount.objects.get(id=account_id, platform='FB')
        graph = facebook.GraphAPI(access_token=account.access_token)
        
        # Fetch posts from the last 30 days
        since_date = datetime.now() - timedelta(days=30)
        posts = graph.get_connections('me', 'posts', since=since_date.timestamp())
        
        for post in posts['data']:
            post_insights = graph.get_connections(post['id'], 'insights')
            
            analytics, created = PostAnalytics.objects.update_or_create(
                account=account,
                post_id=post['id'],
                defaults={
                    'likes_count': post.get('likes', {}).get('summary', {}).get('total_count', 0),
                    'comments_count': post.get('comments', {}).get('summary', {}).get('total_count', 0),
                    'shares_count': post.get('shares', {}).get('count', 0) if 'shares' in post else 0,
                    'reach_count': next((metric['values'][0]['value'] for metric in post_insights['data'] 
                                      if metric['name'] == 'post_impressions_unique'), 0),
                    'posted_at': datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                }
            )
            
            if analytics.reach_count > 0:
                analytics.engagement_rate = ((analytics.likes_count + analytics.comments_count + 
                                           analytics.shares_count) / analytics.reach_count) * 100
                analytics.save()
                
    except Exception as e:
        print(f"Error fetching Facebook insights: {str(e)}")

@shared_task
def fetch_instagram_insights(account_id):
    try:
        account = SocialMediaAccount.objects.get(id=account_id, platform='IG')
        
        # Instagram Graph API endpoint
        base_url = 'https://graph.instagram.com/v12.0'
        
        # Fetch recent media
        media_response = requests.get(
            f"{base_url}/me/media",
            params={
                'access_token': account.access_token,
                'fields': 'id,caption,media_type,timestamp,like_count,comments_count'
            }
        )
        
        if media_response.status_code == 200:
            media_data = media_response.json()
            
            for media in media_data['data']:
                # Fetch insights for each media
                insights_response = requests.get(
                    f"{base_url}/{media['id']}/insights",
                    params={
                        'access_token': account.access_token,
                        'metric': 'reach,impressions'
                    }
                )
                
                if insights_response.status_code == 200:
                    insights_data = insights_response.json()
                    
                    analytics, created = PostAnalytics.objects.update_or_create(
                        account=account,
                        post_id=media['id'],
                        defaults={
                            'likes_count': media.get('like_count', 0),
                            'comments_count': media.get('comments_count', 0),
                            'reach_count': next((metric['values'][0]['value'] for metric in insights_data['data'] 
                                              if metric['name'] == 'reach'), 0),
                            'posted_at': datetime.strptime(media['timestamp'], '%Y-%m-%dT%H:%M:%S+0000'),
                        }
                    )
                    
                    if analytics.reach_count > 0:
                        analytics.engagement_rate = ((analytics.likes_count + analytics.comments_count) / 
                                                   analytics.reach_count) * 100
                        analytics.save()
                        
    except Exception as e:
        print(f"Error fetching Instagram insights: {str(e)}")

@shared_task
def update_engagement_metrics():
    for account in SocialMediaAccount.objects.all():
        try:
            today = datetime.now().date()
            
            if account.platform == 'FB':
                graph = facebook.GraphAPI(access_token=account.access_token)
                insights = graph.get_connections('me', 'insights')
                
                metrics, created = EngagementMetrics.objects.get_or_create(
                    account=account,
                    date=today,
                    defaults={
                        'followers_count': graph.get_object('me')['fan_count'],
                        'profile_views': next((metric['values'][0]['value'] for metric in insights['data'] 
                                            if metric['name'] == 'page_views_total'), 0),
                        'total_reach': next((metric['values'][0]['value'] for metric in insights['data'] 
                                          if metric['name'] == 'page_impressions_unique'), 0),
                        'total_impressions': next((metric['values'][0]['value'] for metric in insights['data'] 
                                                if metric['name'] == 'page_impressions'), 0),
                    }
                )
                
            elif account.platform == 'IG':
                base_url = 'https://graph.instagram.com/v12.0'
                
                profile_response = requests.get(
                    f"{base_url}/me",
                    params={
                        'access_token': account.access_token,
                        'fields': 'followers_count,profile_views'
                    }
                )
                
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    
                    metrics, created = EngagementMetrics.objects.get_or_create(
                        account=account,
                        date=today,
                        defaults={
                            'followers_count': profile_data.get('followers_count', 0),
                            'profile_views': profile_data.get('profile_views', 0),
                            'total_reach': 0,  # These metrics require business account
                            'total_impressions': 0,
                        }
                    )
                    
        except Exception as e:
            print(f"Error updating engagement metrics for account {account.id}: {str(e)}") 