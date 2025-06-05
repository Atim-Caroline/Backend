from django.urls import path
from . import views

app_name = 'trends'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('insights/', views.insight_list, name='insight_list'),
    path('insights/<int:pk>/', views.insight_detail, name='insight_detail'),
    path('alerts/', views.trend_alerts, name='alerts'),
    path('alerts/create/', views.create_alert, name='create_alert'),
    path('alerts/edit/<int:alert_id>/', views.edit_alert, name='edit_alert'),
    path('alerts/delete/<int:alert_id>/', views.delete_alert, name='delete_alert'),
    
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
    
    # API endpoints
    path('api/topics/', views.trending_topics_data, name='api_topics'),
    path('api/topics/refresh/', views.refresh_trends, name='refresh_trends'),
    path('api/notifications/', views.notifications_data, name='api_notifications'),
] 