from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import ScheduledPost, PostReminder
import facebook
import requests

@shared_task
def process_scheduled_posts():
    now = timezone.now()
    scheduled_posts = ScheduledPost.objects.filter(
        status='PENDING',
        scheduled_time__lte=now
    )
    
    for post in scheduled_posts:
        try:
            if post.account.platform == 'FB':
                graph = facebook.GraphAPI(access_token=post.account.access_token)
                
                post_data = {
                    'message': post.content
                }
                
                if post.media_url:
                    post_data['link'] = post.media_url
                    
                response = graph.put_object(
                    parent_object='me',
                    connection_name='feed',
                    **post_data
                )
                
                post.status = 'PUBLISHED'
                post.published_post_id = response.get('id')
                
            elif post.account.platform == 'IG':
                # Instagram Graph API endpoint
                base_url = 'https://graph.instagram.com/v12.0'
                
                if post.media_url:
                    # First, create a container
                    container_response = requests.post(
                        f"{base_url}/me/media",
                        params={
                            'access_token': post.account.access_token,
                            'image_url': post.media_url,
                            'caption': post.content
                        }
                    )
                    
                    if container_response.status_code == 200:
                        container_data = container_response.json()
                        
                        # Then publish the container
                        publish_response = requests.post(
                            f"{base_url}/me/media_publish",
                            params={
                                'access_token': post.account.access_token,
                                'creation_id': container_data['id']
                            }
                        )
                        
                        if publish_response.status_code == 200:
                            post.status = 'PUBLISHED'
                            post.published_post_id = publish_response.json().get('id')
                        else:
                            raise Exception(f"Failed to publish Instagram post: {publish_response.text}")
                    else:
                        raise Exception(f"Failed to create Instagram media container: {container_response.text}")
                else:
                    raise Exception("Instagram posts require media content")
                    
            post.save()
            
        except Exception as e:
            post.status = 'FAILED'
            post.error_message = str(e)
            post.save()

@shared_task
def process_post_reminders():
    now = timezone.now()
    current_time = now.time()
    
    # Process daily reminders
    daily_reminders = PostReminder.objects.filter(
        is_active=True,
        frequency='DAILY',
        preferred_time__lte=current_time,
        last_reminded_at__lt=now.date()
    )
    
    # Process weekly reminders
    weekly_reminders = PostReminder.objects.filter(
        is_active=True,
        frequency='WEEKLY',
        preferred_time__lte=current_time,
        last_reminded_at__lt=now - timedelta(days=7)
    )
    
    # Process monthly reminders
    monthly_reminders = PostReminder.objects.filter(
        is_active=True,
        frequency='MONTHLY',
        preferred_time__lte=current_time,
        last_reminded_at__lt=now - timedelta(days=30)
    )
    
    all_reminders = list(daily_reminders) + list(weekly_reminders) + list(monthly_reminders)
    
    for reminder in all_reminders:
        try:
            send_mail(
                subject=f"Social Media Post Reminder: {reminder.title}",
                message=f"""
                Hello {reminder.user.username},
                
                This is a reminder to create your {reminder.frequency.lower()} social media post:
                
                Title: {reminder.title}
                Description: {reminder.description}
                
                Best regards,
                Your Social Media Assistant
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reminder.user.email],
            )
            
            reminder.last_reminded_at = now
            reminder.save()
            
        except Exception as e:
            print(f"Error processing reminder {reminder.id}: {str(e)}") 