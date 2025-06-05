from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.ScheduledPostViewSet, basename='scheduled-post')
router.register(r'reminders', views.PostReminderViewSet, basename='post-reminder')

urlpatterns = [
    path('', include(router.urls)),
] 