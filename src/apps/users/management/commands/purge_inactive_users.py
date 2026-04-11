"""
Management command: purge_inactive_users
=========================================

GDPR obligation – accounts inactive for more than one year are anonymised:
personal-data fields are cleared and the account is deactivated.  The
database row is kept to preserve referential integrity for published theses,
citations, etc.

Usage
-----
    python manage.py purge_inactive_users
    python manage.py purge_inactive_users --dry-run
    python manage.py purge_inactive_users --days 365

The command considers a user "inactive" when:
  • ``last_activity_at`` is set and is older than ``--days`` days, OR
  • ``last_activity_at`` is NULL and ``date_joined`` is older than ``--days`` days.

Staff and superuser accounts are excluded.
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Anonymise accounts that have been inactive for more than one year (GDPR).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=365,
            help='Number of days of inactivity before anonymisation (default: 365).',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report which accounts would be anonymised without making changes.',
        )

    def handle(self, *args, **options):
        # Import here to avoid app-registry issues during tests
        from apps.users.models import User

        days = options['days']
        dry_run = options['dry_run']
        cutoff = timezone.now() - timedelta(days=days)

        # Accounts that have explicit last_activity_at older than cutoff
        inactive_via_activity = User.objects.filter(
            is_active=True,
            is_staff=False,
            is_superuser=False,
            last_activity_at__lt=cutoff,
        )

        # Accounts that never recorded any activity and joined before cutoff
        inactive_via_join = User.objects.filter(
            is_active=True,
            is_staff=False,
            is_superuser=False,
            last_activity_at__isnull=True,
            date_joined__lt=cutoff,
        )

        candidates = (inactive_via_activity | inactive_via_join).distinct()
        count = candidates.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No inactive accounts found.'))
            return

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'[DRY RUN] {count} account(s) would be anonymised:'
                )
            )
            for user in candidates.order_by('username'):
                last = user.last_activity_at or user.date_joined
                self.stdout.write(f'  • {user.username} (last active: {last.date()})')
            return

        anonymised = 0
        for user in candidates:
            pk = user.pk
            user.username = f'deleted_{pk}'
            user.email = ''
            user.real_name = ''
            user.bio = ''
            user.linkedin_url = ''
            user.orcid_url = ''
            user.website_url = ''
            user.is_active = False
            user.deletion_requested_at = timezone.now()
            user.set_unusable_password()
            user.save(update_fields=[
                'username', 'email', 'real_name', 'bio',
                'linkedin_url', 'orcid_url', 'website_url',
                'is_active', 'deletion_requested_at', 'password',
            ])
            anonymised += 1
            self.stdout.write(f'  Anonymised pk={pk}')

        self.stdout.write(
            self.style.SUCCESS(f'Done. {anonymised} account(s) anonymised.')
        )
