from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
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


class UserProfileForm(forms.ModelForm):
    """Edit own profile: display name, bio, and public links."""

    class Meta:
        model = User
        fields = ('real_name', 'bio', 'linkedin_url', 'orcid_url', 'website_url')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class DeleteAccountForm(forms.Form):
    """Confirms account deletion by requiring current password."""

    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm your password',
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not authenticate(username=self.user.username, password=password):
            raise forms.ValidationError('Password is incorrect.')
        return password
