from django.urls import path
from . import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('calendar/', views.calendar_view, name='calendar'),
    
    path('reminders/', views.reminders, name='reminders'),
    path('reminders/create/', views.create_reminder, name='create_reminder'),
    path('reminders/edit/<int:reminder_id>/', views.edit_reminder, name='edit_reminder'),
    path('reminders/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    
    # API endpoints
    path('api/posts/', views.scheduled_posts_data, name='api_posts'),
    path('api/reminders/', views.reminders_data, name='api_reminders'),
] 