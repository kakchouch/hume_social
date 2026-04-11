from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Signup form for the custom user model."""

    sponsor_username = forms.CharField(
        required=True,
        help_text='Enter the username of your sponsor.',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'real_name', 'email')

    def clean_sponsor_username(self):
        sponsor_username = (self.cleaned_data.get('sponsor_username') or '').strip()
        try:
            sponsor = User.objects.get(username=sponsor_username)
        except User.DoesNotExist:
            raise forms.ValidationError('Sponsor username was not found.')
        return sponsor

    def save(self, commit=True):
        user = super().save(commit=False)
        user.sponsor = self.cleaned_data['sponsor_username']
        user.sponsorship_status = User.SponsorshipStatus.PENDING
        if commit:
            user.save()
        return user
