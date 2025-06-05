from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from social_connector.views import SocialAccountViewSet, SocialPostViewSet
from compliance_service.views import ContentRuleViewSet, ComplianceCheckViewSet, ComplianceReportViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'social/accounts', SocialAccountViewSet, basename='social-account')
router.register(r'social/posts', SocialPostViewSet, basename='social-post')
router.register(r'compliance/rules', ContentRuleViewSet, basename='content-rule')
router.register(r'compliance/checks', ComplianceCheckViewSet, basename='compliance-check')
router.register(r'compliance/reports', ComplianceReportViewSet, basename='compliance-report')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api_token'),
    path('api/scheduler/', include('scheduler.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 