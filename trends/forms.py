from django import forms
from .models import UserTrendAlert

class UserTrendAlertForm(forms.ModelForm):
    class Meta:
        model = UserTrendAlert
        fields = ['keywords', 'platforms', 'min_volume', 'is_active']
        widgets = {
            'keywords': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter comma-separated keywords'}),
            'platforms': forms.TextInput(attrs={'placeholder': 'Enter comma-separated platforms (FB, IG, ALL)'}),
        }
        help_texts = {
            'keywords': 'Enter keywords separated by commas (e.g., "marketing, social media, digital")',
            'platforms': 'Enter platforms separated by commas (e.g., "FB, IG, ALL")',
            'min_volume': 'Minimum number of mentions to trigger an alert',
        } 