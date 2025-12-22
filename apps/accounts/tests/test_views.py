from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.users.models import Profile

User = get_user_model()


class ProfileViewTests(TestCase):
    """Test cases for ProfileView"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.profile_url = reverse("account_profile")

    def test_profile_view_requires_login(self):
        """Test that profile view requires authentication"""
        response = self.client.get(self.profile_url)
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_profile_view_accessible_when_logged_in(self):
        """Test that profile view is accessible when user is logged in"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_profile_view_uses_correct_template(self):
        """Test that profile view uses the correct template"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.profile_url)
        self.assertTemplateUsed(response, "account/profile.html")

    def test_profile_view_context_without_profile(self):
        """Test that profile view context includes user when profile doesn't exist"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.context)
        self.assertEqual(response.context["user"], self.user)
        # Profile should be in context, but None if it doesn't exist
        self.assertIn("profile", response.context)
        self.assertIsNone(response.context["profile"])

    def test_profile_view_context_with_profile(self):
        """Test that profile view context includes user and profile when profile exists"""
        # Create a profile for the user
        profile = Profile.objects.create(user=self.user, phone="+256781435857")
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.context)
        self.assertIn("profile", response.context)
        self.assertEqual(response.context["user"], self.user)
        self.assertEqual(response.context["profile"], profile)

    def test_profile_view_displays_user_information(self):
        """Test that profile view displays user information in the template"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.profile_url)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)

    def test_profile_view_displays_profile_phone_when_exists(self):
        """Test that profile view displays phone number when profile exists"""
        phone = "+256781435857"
        Profile.objects.create(user=self.user, phone=phone)
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.profile_url)
        # Phone number should be displayed in the template
        # Check for the phone number (may be formatted by PhoneNumberField)
        response_content = response.content.decode()
        # PhoneNumberField displays as string, check for phone or digits
        phone_digits = "256781435857"
        self.assertTrue(
            phone in response_content or phone_digits in response_content,
            f"Phone number {phone} not found in response",
        )


class PhoneChangeViewTests(TestCase):
    """Test cases for PhoneChangeView"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.phone_change_url = reverse("account_change_phone")

    def test_phone_change_view_requires_login(self):
        """Test that phone change view requires authentication"""
        response = self.client.get(self.phone_change_url)
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_phone_change_view_accessible_when_logged_in(self):
        """Test that phone change view is accessible when user is logged in"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.phone_change_url)
        self.assertEqual(response.status_code, 200)

    def test_phone_change_view_uses_correct_template(self):
        """Test that phone change view uses the correct template"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.phone_change_url)
        self.assertTemplateUsed(response, "account/phone_change.html")

    def test_phone_change_view_context_without_profile(self):
        """Test that phone change view context is correct when profile doesn't exist"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.phone_change_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.context)
        self.assertIn("form", response.context)
        self.assertEqual(response.context["user"], self.user)
        self.assertIsNone(response.context.get("phone"))
        self.assertFalse(response.context.get("phone_verified", True))

    def test_phone_change_view_context_with_profile(self):
        """Test that phone change view context includes phone when profile exists"""
        phone = "+256781435857"
        Profile.objects.create(user=self.user, phone=phone)
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.phone_change_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("phone", response.context)
        self.assertEqual(str(response.context["phone"]), phone)
        self.assertTrue(response.context.get("phone_verified", False))

    def test_phone_change_view_initial_data_with_existing_phone(self):
        """Test that phone change view pre-fills form with existing phone number"""
        phone = "+256781435857"
        Profile.objects.create(user=self.user, phone=phone)
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.phone_change_url)
        form = response.context["form"]
        # Check that initial data is set
        self.assertEqual(str(form.initial.get("phone", "")), phone)

    def test_phone_change_post_with_valid_phone(self):
        """Test that phone change view updates phone number with valid data"""
        self.client.login(username="testuser", password="testpass123")
        new_phone = "+256781435857"
        response = self.client.post(self.phone_change_url, {"phone": new_phone})
        # Should redirect to profile page
        if response.status_code != 302:
            # If not redirecting, form might be invalid - check form errors
            if hasattr(response, "context") and "form" in response.context:
                form = response.context["form"]
                self.fail(f"Form is invalid. Errors: {form.errors}")
        self.assertEqual(response.status_code, 302, f"Expected redirect but got {response.status_code}")
        self.assertEqual(response.url, reverse("account_profile"))
        # Check that profile was created/updated
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile.phone), new_phone)

    def test_phone_change_post_creates_profile_if_not_exists(self):
        """Test that phone change view creates profile if it doesn't exist"""
        self.client.login(username="testuser", password="testpass123")
        new_phone = "+256781435857"
        # Profile shouldn't exist yet
        self.assertFalse(Profile.objects.filter(user=self.user).exists())
        response = self.client.post(self.phone_change_url, {"phone": new_phone})
        # Should redirect to profile page
        if response.status_code != 302:
            # If not redirecting, form might be invalid - check form errors
            if hasattr(response, "context") and "form" in response.context:
                form = response.context["form"]
                self.fail(f"Form is invalid. Errors: {form.errors}")
        self.assertEqual(response.status_code, 302, f"Expected redirect but got {response.status_code}")
        # Profile should be created
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile.phone), new_phone)

    def test_phone_change_post_updates_existing_profile(self):
        """Test that phone change view updates existing profile"""
        existing_phone = "+256781435857"
        Profile.objects.create(user=self.user, phone=existing_phone)
        self.client.login(username="testuser", password="testpass123")
        new_phone = "+256781435858"  # Different valid phone number
        response = self.client.post(self.phone_change_url, {"phone": new_phone})
        # Should redirect
        if response.status_code != 302:
            # If not redirecting, form might be invalid - check form errors
            if hasattr(response, "context") and "form" in response.context:
                form = response.context["form"]
                self.fail(f"Form is invalid. Errors: {form.errors}")
        self.assertEqual(response.status_code, 302, f"Expected redirect but got {response.status_code}")
        # Phone should be updated
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile.phone), new_phone)
        self.assertNotEqual(str(profile.phone), existing_phone)

    def test_phone_change_post_with_invalid_phone(self):
        """Test that phone change view shows errors with invalid phone number"""
        self.client.login(username="testuser", password="testpass123")
        invalid_phone = "123"  # Invalid phone number
        response = self.client.post(self.phone_change_url, {"phone": invalid_phone})
        # Should not redirect, should show form with errors
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_phone_change_post_with_empty_phone(self):
        """Test that phone change view accepts empty phone (since it's not required)"""
        # Create profile with existing phone
        Profile.objects.create(user=self.user, phone="+1234567890")
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(self.phone_change_url, {"phone": ""})
        # Should redirect (empty phone is valid since field is not required)
        self.assertEqual(response.status_code, 302)
        profile = Profile.objects.get(user=self.user)
        # Phone should be cleared (empty string becomes None)
        # PhoneNumberField may return empty string or None
        phone_value = profile.phone
        self.assertTrue(phone_value is None or str(phone_value) == "")

    def test_phone_change_post_success_message(self):
        """Test that phone change view shows success message after update"""
        self.client.login(username="testuser", password="testpass123")
        new_phone = "+256781435857"
        # Post without follow to check redirect
        response = self.client.post(self.phone_change_url, {"phone": new_phone})
        # Check if form is invalid
        if response.status_code != 302:
            if hasattr(response, "context") and "form" in response.context:
                form = response.context["form"]
                self.fail(f"Form is invalid. Errors: {form.errors}")
        self.assertEqual(response.status_code, 302, f"Expected redirect but got {response.status_code}")
        # Now follow the redirect and check messages
        response = self.client.get(response.url, follow=True)
        # Messages should be in the context after following redirect
        messages_list = list(response.context.get("messages", []))
        # If not in context, try getting from session
        if not messages_list:
            # Access messages from the session storage
            from django.contrib.messages.storage.fallback import FallbackStorage

            storage = FallbackStorage(response.wsgi_request)
            messages_list = list(storage)

        self.assertTrue(len(messages_list) > 0, "No messages found in response")
        success_messages = [
            m
            for m in messages_list
            if (hasattr(m, "level_tag") and m.level_tag == "success") or (hasattr(m, "level") and m.level == 25)
        ]
        msg = f"No success messages found. Messages: {[str(m) for m in messages_list]}"
        self.assertTrue(len(success_messages) > 0, msg)
        message_text = str(success_messages[0])
        self.assertIn("Phone number updated successfully", message_text)

    def test_phone_change_view_displays_current_phone(self):
        """Test that phone change view displays current phone number in template"""
        phone = "+256781435857"
        Profile.objects.create(user=self.user, phone=phone)
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.phone_change_url)
        # Should display current phone
        self.assertContains(response, phone)

    def test_phone_change_view_displays_form(self):
        """Test that phone change view displays the phone change form"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.phone_change_url)
        # Should contain form elements
        self.assertContains(response, "phone", count=None)  # Phone field should be present
        self.assertContains(response, "Change Phone")  # Submit button text
