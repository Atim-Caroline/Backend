from django import forms
from .models import ScheduledPost, PostReminder

class ScheduledPostForm(forms.ModelForm):
    class Meta:
        model = ScheduledPost
        fields = ['title', 'content', 'scheduled_time', 'image']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PostReminderForm(forms.ModelForm):
    class Meta:
        model = PostReminder
        fields = ['title', 'description', 'frequency', 'preferred_time']
        widgets = {
            'preferred_time': forms.TimeInput(attrs={'type': 'time'}),
        } 