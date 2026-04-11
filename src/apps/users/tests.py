from django.test import TestCase
from django.urls import reverse

from apps.users.models import ContactRequest, User
from apps.theses.models import MiniThesis


class TestUserModel(TestCase):
    """Test cases for the custom User model."""

    def test_user_creation(self):
        """Test that a user can be created."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_levels(self):
        """Test user level permissions."""
        reader = User.objects.create_user(
            username='reader', level=User.UserLevel.READER
        )
        commentator = User.objects.create_user(
            username='commentator', level=User.UserLevel.COMMENTATOR
        )
        tagger = User.objects.create_user(
            username='tagger', level=User.UserLevel.TAGGER
        )
        reviewer = User.objects.create_user(
            username='reviewer', level=User.UserLevel.EDITORIAL_REVIEWER
        )

        # Test permissions
        self.assertFalse(reader.can_comment())
        self.assertTrue(commentator.can_comment())
        self.assertTrue(tagger.can_comment())
        self.assertTrue(reviewer.can_comment())

        self.assertFalse(reader.can_tag())
        self.assertFalse(commentator.can_tag())
        self.assertTrue(tagger.can_tag())
        self.assertTrue(reviewer.can_tag())

        self.assertFalse(reader.can_review())
        self.assertFalse(commentator.can_review())
        self.assertFalse(tagger.can_review())
        self.assertTrue(reviewer.can_review())

    def test_tag_accuracy_score_bounds(self):
        """Test that tag accuracy score stays within bounds."""
        user = User.objects.create_user(username='testuser')

        # Test upper bound
        user.bounded_tag_accuracy_score = 3.0
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.tag_accuracy_score, 2.0)

        # Test lower bound
        user.bounded_tag_accuracy_score = -1.0
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.tag_accuracy_score, 0.0)


class TestUserPages(TestCase):
    """Test users list and detail pages."""

    def setUp(self):
        self.sponsor = User.objects.create_user(
            username='sponsor1',
            real_name='Sponsor Person',
            email='sponsor@example.com',
        )
        self.user = User.objects.create_user(
            username='alice',
            real_name='Alice Doe',
            email='alice@example.com',
            sponsor=self.sponsor,
            linkedin_url='https://www.linkedin.com/in/alice',
        )

    def test_user_list_page_loads(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User Directory')
        self.assertContains(response, 'alice')

    def test_user_list_search_filters(self):
        response = self.client.get(reverse('users:list'), {'q': 'alice'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alice')
        self.assertNotContains(response, 'sponsor1')

    def test_user_detail_shows_sponsor_and_contacts(self):
        response = self.client.get(reverse('users:detail', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice Doe')
        self.assertContains(response, 'LinkedIn')
        self.assertContains(response, 'Sponsor Person')

    def test_user_profile_can_send_contact_request(self):
        requester = User.objects.create_user(username='requester')
        self.client.force_login(requester)

        response = self.client.post(
            reverse('users:send_contact_request', args=[self.user.pk]),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ContactRequest.objects.filter(
                from_user=requester,
                to_user=self.user,
                status=ContactRequest.Status.PENDING,
            ).exists()
        )

    def test_accepting_contact_request_adds_contact(self):
        requester = User.objects.create_user(username='requester')
        contact_request = ContactRequest.objects.create(
            from_user=requester,
            to_user=self.user,
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('users:contact_request_decision', args=[contact_request.pk]),
            {'decision': 'accept'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        contact_request.refresh_from_db()
        self.assertEqual(contact_request.status, ContactRequest.Status.ACCEPTED)
        self.assertTrue(self.user.contacts.filter(pk=requester.pk).exists())

    def test_landing_shows_signup_for_anonymous(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create your account')

    def test_landing_hides_signup_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Signed in as')
        self.assertNotContains(response, 'Create your account')

    def test_landing_shows_feed_for_authenticated_user(self):
        MiniThesis.objects.create(
            author=self.user,
            thesis='Visible feed thesis',
            facts='Facts',
            normative_premises='Premises',
            conclusion='Conclusion',
            declared_limits='Limits',
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your feed')
        self.assertContains(response, 'Visible feed thesis')

    def test_feed_page_redirects_to_homepage(self):
        response = self.client.get(reverse('feed:index'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_signin_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign in')

    def test_signin_page_authenticates_user(self):
        login_user = User.objects.create_user(
            username='login_user',
            password='StrongPass!23',
        )
        response = self.client.post(
            reverse('login'),
            {'username': 'login_user', 'password': 'StrongPass!23'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Signed in as')
        self.assertIn(str(login_user.pk), self.client.session.get('_auth_user_id', ''))

    def test_landing_signup_creates_account(self):
        payload = {
            'username': 'newjoiner',
            'real_name': 'New Joiner',
            'email': 'newjoiner@example.com',
            'sponsor_username': 'sponsor1',
            'password1': 'Str0ngPass!234',
            'password2': 'Str0ngPass!234',
        }
        response = self.client.post(reverse('index'), payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newjoiner').exists())
        new_user = User.objects.get(username='newjoiner')
        self.assertEqual(new_user.sponsor, self.sponsor)
        self.assertEqual(new_user.sponsorship_status, User.SponsorshipStatus.PENDING)

    def test_landing_signup_requires_existing_sponsor(self):
        payload = {
            'username': 'no_sponsor_user',
            'real_name': 'No Sponsor',
            'email': 'nosponsor@example.com',
            'sponsor_username': 'unknown_sponsor',
            'password1': 'Str0ngPass!234',
            'password2': 'Str0ngPass!234',
        }
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sponsor username was not found')
        self.assertFalse(User.objects.filter(username='no_sponsor_user').exists())

    def test_sponsor_can_approve_pending_user(self):
        pending_user = User.objects.create_user(
            username='pending_user',
            sponsor=self.sponsor,
            sponsorship_status=User.SponsorshipStatus.PENDING,
        )
        self.client.force_login(self.sponsor)
        response = self.client.post(
            reverse('users:sponsorship_decision', args=[pending_user.pk]),
            {'decision': 'approve'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        pending_user.refresh_from_db()
        self.assertEqual(pending_user.sponsorship_status, User.SponsorshipStatus.APPROVED)

    def test_sponsor_can_reject_pending_user(self):
        pending_user = User.objects.create_user(
            username='pending_user2',
            sponsor=self.sponsor,
            sponsorship_status=User.SponsorshipStatus.PENDING,
        )
        self.client.force_login(self.sponsor)
        response = self.client.post(
            reverse('users:sponsorship_decision', args=[pending_user.pk]),
            {'decision': 'reject'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        pending_user.refresh_from_db()
        self.assertEqual(pending_user.sponsorship_status, User.SponsorshipStatus.REJECTED)


class TestGDPRViews(TestCase):
    """Tests for my-profile, delete-account, data-download and cookie-consent."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='gdpr_user',
            email='gdpr@example.com',
            password='Pass1234!',
        )
        self.client.force_login(self.user)

    def test_my_profile_renders(self):
        response = self.client.get(reverse('users:me'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit profile')

    def test_my_profile_edit_saves(self):
        response = self.client.post(
            reverse('users:me'),
            {'real_name': 'Updated Name', 'bio': 'Hello', 'linkedin_url': '',
             'orcid_url': '', 'website_url': ''},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.real_name, 'Updated Name')

    def test_delete_account_get_renders(self):
        response = self.client.get(reverse('users:delete_account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete your account')

    def test_delete_account_wrong_password_rejected(self):
        response = self.client.post(
            reverse('users:delete_account'),
            {'password': 'WrongPass!'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password is incorrect')
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_delete_account_correct_password_anonymises(self):
        response = self.client.post(
            reverse('users:delete_account'),
            {'password': 'Pass1234!'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account deleted')
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(self.user.email, '')
        self.assertTrue(self.user.username.startswith('deleted_'))

    def test_download_my_data_returns_json(self):
        response = self.client.get(reverse('users:download_my_data'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('attachment', response['Content-Disposition'])
        import json
        data = json.loads(response.content)
        self.assertIn('profile', data)
        self.assertEqual(data['profile']['username'], 'gdpr_user')

    def test_cookie_consent_sets_session(self):
        response = self.client.post(
            reverse('users:cookie_consent'),
            {'next': '/'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get('cookies_consented'))

    def test_my_profile_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('users:me'))
        self.assertEqual(response.status_code, 302)


class TestPurgeInactiveUsers(TestCase):
    """Tests for the purge_inactive_users management command."""

    def test_dry_run_reports_without_deleting(self):
        from datetime import timedelta
        from django.utils import timezone
        from django.core.management import call_command
        from io import StringIO

        old_user = User.objects.create_user(
            username='old_inactive',
            last_activity_at=timezone.now() - timedelta(days=400),
        )
        out = StringIO()
        call_command('purge_inactive_users', '--dry-run', '--days', '365', stdout=out)
        output = out.getvalue()
        self.assertIn('old_inactive', output)
        old_user.refresh_from_db()
        self.assertTrue(old_user.is_active)  # not touched

    def test_purge_anonymises_inactive_user(self):
        from datetime import timedelta
        from django.utils import timezone
        from django.core.management import call_command

        old_user = User.objects.create_user(
            username='really_old',
            email='old@example.com',
            last_activity_at=timezone.now() - timedelta(days=400),
        )
        call_command('purge_inactive_users', '--days', '365', verbosity=0)
        old_user.refresh_from_db()
        self.assertFalse(old_user.is_active)
        self.assertEqual(old_user.email, '')
