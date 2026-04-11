from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for custom User model."""

    list_display = (
        'username', 'email', 'real_name', 'level',
        'is_founder', 'tag_accuracy_score'
    )
    list_filter = ('level', 'is_founder', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'real_name')

    fieldsets = UserAdmin.fieldsets + (
        ('Hume Profile', {
            'fields': (
                'real_name', 'bio', 'linkedin_url', 'orcid_url',
                'website_url', 'level', 'is_founder', 'tag_accuracy_score'
            )
        }),
        ('Sponsorship', {
            'fields': ('sponsor',)
        }),
    )

    readonly_fields = ('tag_accuracy_score',)
