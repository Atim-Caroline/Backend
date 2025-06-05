from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import SocialMediaAccount, PostAnalytics, EngagementMetrics, AnalyticsReport, Metric

@login_required
def dashboard(request):
    reports = AnalyticsReport.objects.filter(user=request.user)[:5]
    return render(request, 'analytics/dashboard.html', {'reports': reports})

@login_required
def post_analytics(request):
    return render(request, 'analytics/post_analytics.html')

@login_required
def engagement_metrics(request):
    return render(request, 'analytics/engagement_metrics.html')

@login_required
def social_accounts(request):
    accounts = SocialMediaAccount.objects.filter(user=request.user)
    return render(request, 'analytics/social_accounts.html', {'accounts': accounts})

@login_required
def export_data(request):
    # Implementation for data export
    return JsonResponse({'status': 'success'})

@login_required
def post_analytics_data(request, account_id):
    analytics = PostAnalytics.objects.filter(account_id=account_id)
    data = [{
        'post_id': a.post_id,
        'likes': a.likes_count,
        'comments': a.comments_count,
        'shares': a.shares_count,
        'reach': a.reach_count,
        'engagement_rate': a.engagement_rate,
        'posted_at': a.posted_at.isoformat()
    } for a in analytics]
    return JsonResponse({'data': data})

@login_required
def engagement_data(request, account_id):
    metrics = EngagementMetrics.objects.filter(account_id=account_id)
    data = [{
        'date': m.date.isoformat(),
        'followers': m.followers_count,
        'views': m.profile_views,
        'reach': m.total_reach,
        'impressions': m.total_impressions
    } for m in metrics]
    return JsonResponse({'data': data})

@login_required
def refresh_analytics(request, account_id):
    # Trigger Celery task to refresh analytics
    from .tasks import fetch_facebook_insights, fetch_instagram_insights
    account = SocialMediaAccount.objects.get(id=account_id)
    
    if account.platform == 'FB':
        fetch_facebook_insights.delay(account_id)
    elif account.platform == 'IG':
        fetch_instagram_insights.delay(account_id)
        
    return JsonResponse({'status': 'refresh_started'})

@login_required
def report_list(request):
    reports = AnalyticsReport.objects.filter(user=request.user)
    return render(request, 'analytics/report_list.html', {'reports': reports})

@login_required
def report_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        report = AnalyticsReport.objects.create(
            user=request.user,
            title=title,
            description=description
        )
        messages.success(request, 'Report created successfully.')
        return redirect('analytics:report_detail', pk=report.pk)
    return render(request, 'analytics/report_form.html')

@login_required
def report_detail(request, pk):
    report = get_object_or_404(AnalyticsReport, pk=pk, user=request.user)
    metrics = report.metrics.all()
    return render(request, 'analytics/report_detail.html', {
        'report': report,
        'metrics': metrics
    })

@login_required
def report_edit(request, pk):
    report = get_object_or_404(AnalyticsReport, pk=pk, user=request.user)
    if request.method == 'POST':
        report.title = request.POST.get('title')
        report.description = request.POST.get('description')
        report.save()
        messages.success(request, 'Report updated successfully.')
        return redirect('analytics:report_detail', pk=report.pk)
    return render(request, 'analytics/report_form.html', {'report': report})

@login_required
def report_delete(request, pk):
    report = get_object_or_404(AnalyticsReport, pk=pk, user=request.user)
    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted successfully.')
        return redirect('analytics:report_list')
    return render(request, 'analytics/report_confirm_delete.html', {'report': report}) 