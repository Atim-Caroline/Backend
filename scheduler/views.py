from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ScheduledPost, PostReminder, PostAnalytics
from .forms import ScheduledPostForm, PostReminderForm
from django.contrib import messages
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .serializers import ScheduledPostSerializer, PostReminderSerializer

@login_required
def dashboard(request):
    upcoming_posts = ScheduledPost.objects.filter(user=request.user, status='scheduled')[:5]
    return render(request, 'scheduler/dashboard.html', {'posts': upcoming_posts})

@login_required
def post_list(request):
    posts = ScheduledPost.objects.filter(user=request.user)
    return render(request, 'scheduler/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        scheduled_time = request.POST.get('scheduled_time')
        image = request.FILES.get('image')
        
        post = ScheduledPost.objects.create(
            user=request.user,
            title=title,
            content=content,
            scheduled_time=scheduled_time,
            image=image,
            status='scheduled'
        )
        messages.success(request, 'Post scheduled successfully.')
        return redirect('scheduler:post_detail', pk=post.pk)
    return render(request, 'scheduler/post_form.html')

@login_required
def post_detail(request, pk):
    post = get_object_or_404(ScheduledPost, pk=pk, user=request.user)
    analytics = PostAnalytics.objects.filter(post=post).first()
    return render(request, 'scheduler/post_detail.html', {
        'post': post,
        'analytics': analytics
    })

@login_required
def post_edit(request, pk):
    post = get_object_or_404(ScheduledPost, pk=pk, user=request.user)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.scheduled_time = request.POST.get('scheduled_time')
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.save()
        messages.success(request, 'Post updated successfully.')
        return redirect('scheduler:post_detail', pk=post.pk)
    return render(request, 'scheduler/post_form.html', {'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(ScheduledPost, pk=pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('scheduler:post_list')
    return render(request, 'scheduler/post_confirm_delete.html', {'post': post})

@login_required
def calendar_view(request):
    posts = ScheduledPost.objects.filter(user=request.user)
    return render(request, 'scheduler/calendar.html', {'posts': posts})

@login_required
def scheduled_posts(request):
    posts = ScheduledPost.objects.filter(user=request.user)
    return render(request, 'scheduler/posts.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = ScheduledPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('scheduler:posts')
    else:
        form = ScheduledPostForm()
    return render(request, 'scheduler/post_form.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(ScheduledPost, id=post_id, user=request.user)
    if request.method == 'POST':
        form = ScheduledPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('scheduler:posts')
    else:
        form = ScheduledPostForm(instance=post)
    return render(request, 'scheduler/post_form.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(ScheduledPost, id=post_id, user=request.user)
    post.delete()
    return redirect('scheduler:posts')

@login_required
def reminders(request):
    reminders = PostReminder.objects.filter(user=request.user)
    return render(request, 'scheduler/reminders.html', {'reminders': reminders})

@login_required
def create_reminder(request):
    if request.method == 'POST':
        form = PostReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            return redirect('scheduler:reminders')
    else:
        form = PostReminderForm()
    return render(request, 'scheduler/reminder_form.html', {'form': form})

@login_required
def edit_reminder(request, reminder_id):
    reminder = get_object_or_404(PostReminder, id=reminder_id, user=request.user)
    if request.method == 'POST':
        form = PostReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('scheduler:reminders')
    else:
        form = PostReminderForm(instance=reminder)
    return render(request, 'scheduler/reminder_form.html', {'form': form, 'reminder': reminder})

@login_required
def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(PostReminder, id=reminder_id, user=request.user)
    reminder.delete()
    return redirect('scheduler:reminders')

@login_required
def scheduled_posts_data(request):
    posts = ScheduledPost.objects.filter(user=request.user)
    data = [{
        'id': p.id,
        'content': p.content,
        'scheduled_time': p.scheduled_time.isoformat(),
        'status': p.status,
        'platform': p.account.get_platform_display()
    } for p in posts]
    return JsonResponse({'data': data})

@login_required
def reminders_data(request):
    reminders = PostReminder.objects.filter(user=request.user)
    data = [{
        'id': r.id,
        'title': r.title,
        'description': r.description,
        'frequency': r.frequency,
        'preferred_time': r.preferred_time.strftime('%H:%M')
    } for r in reminders]
    return JsonResponse({'data': data})

class ScheduledPostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScheduledPostSerializer

    def get_queryset(self):
        return ScheduledPost.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming(self):
        upcoming_posts = self.get_queryset().filter(
            scheduled_time__gt=timezone.now(),
            status='scheduled'
        ).order_by('scheduled_time')
        serializer = self.get_serializer(upcoming_posts, many=True)
        return Response(serializer.data)

class PostReminderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostReminderSerializer

    def get_queryset(self):
        return PostReminder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 