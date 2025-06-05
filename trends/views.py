from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import TrendingTopic, UserTrendAlert, TrendNotification, TrendInsight
from .forms import UserTrendAlertForm

@login_required
def trending_topics(request):
    topics = TrendingTopic.objects.all().order_by('-created_at')[:50]
    return render(request, 'trends/topics.html', {'topics': topics})

@login_required
def trend_alerts(request):
    alerts = UserTrendAlert.objects.filter(user=request.user)
    return render(request, 'trends/alerts.html', {'alerts': alerts})

@login_required
def create_alert(request):
    if request.method == 'POST':
        form = UserTrendAlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user
            alert.save()
            return redirect('trends:alerts')
    else:
        form = UserTrendAlertForm()
    return render(request, 'trends/alert_form.html', {'form': form})

@login_required
def edit_alert(request, alert_id):
    alert = get_object_or_404(UserTrendAlert, id=alert_id, user=request.user)
    if request.method == 'POST':
        form = UserTrendAlertForm(request.POST, instance=alert)
        if form.is_valid():
            form.save()
            return redirect('trends:alerts')
    else:
        form = UserTrendAlertForm(instance=alert)
    return render(request, 'trends/alert_form.html', {'form': form, 'alert': alert})

@login_required
def delete_alert(request, alert_id):
    alert = get_object_or_404(UserTrendAlert, id=alert_id, user=request.user)
    alert.delete()
    return redirect('trends:alerts')

@login_required
def notifications(request):
    notifications = TrendNotification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'trends/notifications.html', {'notifications': notifications})

@login_required
def mark_notifications_read(request):
    if request.method == 'POST':
        TrendNotification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def trending_topics_data(request):
    topics = TrendingTopic.objects.all().order_by('-created_at')[:50]
    data = [{
        'topic': t.topic,
        'platform': t.get_platform_display(),
        'volume': t.volume,
        'sentiment': t.sentiment_score,
        'region': t.region,
        'created_at': t.created_at.isoformat()
    } for t in topics]
    return JsonResponse({'data': data})

@login_required
def refresh_trends(request):
    # Trigger Celery task to refresh trends
    from .tasks import fetch_trending_topics
    fetch_trending_topics.delay()
    return JsonResponse({'status': 'refresh_started'})

@login_required
def notifications_data(request):
    notifications = TrendNotification.objects.filter(user=request.user).order_by('-created_at')
    data = [{
        'id': n.id,
        'text': n.notification_text,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat()
    } for n in notifications]
    return JsonResponse({'data': data})

@login_required
def dashboard(request):
    topics = TrendingTopic.objects.all()[:5]
    insights = TrendInsight.objects.all()[:5]
    return render(request, 'trends/dashboard.html', {
        'topics': topics,
        'insights': insights
    })

@login_required
def topic_list(request):
    topics = TrendingTopic.objects.all()
    return render(request, 'trends/topic_list.html', {'topics': topics})

@login_required
def topic_detail(request, pk):
    topic = get_object_or_404(TrendingTopic, pk=pk)
    insights = topic.insights.all()
    return render(request, 'trends/topic_detail.html', {
        'topic': topic,
        'insights': insights
    })

@login_required
def insight_list(request):
    insights = TrendInsight.objects.all()
    return render(request, 'trends/insight_list.html', {'insights': insights})

@login_required
def insight_detail(request, pk):
    insight = get_object_or_404(TrendInsight, pk=pk)
    return render(request, 'trends/insight_detail.html', {'insight': insight}) 