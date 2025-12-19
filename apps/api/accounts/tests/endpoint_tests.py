import re

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AccountEndpointTests(APITestCase):
    def setUp(self):
        self.registration_url = "/api/accounts/registration/"

        # Clear the email outbox before each test
        mail.outbox.clear()

    def test_registration_endpoint_accessible(self):
        """Test that the registration endpoint is accessible without AttributeError"""
        response = self.client.get(self.registration_url)
        # Should return 405 Method Not Allowed for GET, but not AttributeError
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_registration_serializer_has_phone_field_attribute(self):
        """Test that RegisterSerializer has the required _has_phone_field attribute"""
        from apps.api.accounts.serializers import RegisterSerializer

        serializer = RegisterSerializer()
        self.assertTrue(hasattr(serializer, "_has_phone_field"))
        self.assertTrue(serializer._has_phone_field)

    def test_create_account(self):
        data = {
            "email": "testuser@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.registration_url, data, format="json")

        response_keys = ["access", "refresh", "user"]

        self.assertEqual(response.status_code, 201)
        for key in response_keys:
            self.assertTrue(key in response.data)
        self.assertEqual(response.data["user"]["email"], data["email"])
        self.assertEqual(response.data["user"]["username"], "testuser")
        self.assertEqual(response.data["user"]["is_active"], True)
        self.assertEqual(response.data["user"]["is_staff"], False)
        self.assertEqual(response.data["user"]["is_superuser"], False)

        email = EmailAddress.objects.get(email=data["email"])
        self.assertEqual(email.verified, False)

    def test_create_account_with_username_requires_email(self):
        data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.registration_url, data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertTrue("email" in response.data)
        self.assertEqual(response.data, {"email": ["This field is required."]})

    def test_create_account_with_username_and_email(self):
        data = {
            "username": "testuser",
            "email": "test@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.registration_url, data, format="json")

        response_keys = ["access", "refresh", "user"]

        self.assertEqual(response.status_code, 201)
        for key in response_keys:
            self.assertTrue(key in response.data)
        self.assertEqual(response.data["user"]["email"], data["email"])
        self.assertEqual(response.data["user"]["username"], data["username"])
        self.assertEqual(response.data["user"]["is_active"], True)
        self.assertEqual(response.data["user"]["is_staff"], False)
        self.assertEqual(response.data["user"]["is_superuser"], False)

    def test_created_user_can_login(self):
        data = {
            "email": "test@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.registration_url, data, format="json")

        self.assertEqual(response.status_code, 201)

        url = reverse("accounts:login")
        login_data = {
            "email": data["email"],
            "password": data["password1"],
        }

        response = self.client.post(url, login_data, format="json")

        response_keys = ["access", "refresh", "user"]

        self.assertEqual(response.status_code, 200)
        for key in response_keys:
            self.assertTrue(key in response.data)
        self.assertEqual(response.data["user"]["email"], data["email"])
        self.assertEqual(response.data["user"]["is_active"], True)

    def test_created_user_is_automatically_logged_in(self):
        data = {
            "email": "test@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.registration_url, data, format="json")

        self.assertEqual(response.status_code, 201)

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # access the user endpoint to check if the user is logged in
        url = reverse("accounts:user_details")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_user_can_change_password(self):
        data = {
            "email": "test@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.registration_url, data, format="json")

        self.assertEqual(response.status_code, 201)

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # access the user endpoint to check if the user is logged in
        url = reverse("accounts:user_details")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # change password
        url = reverse("accounts:password_change")
        data = {
            "new_password1": "testing321",
            "new_password2": "testing321",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        # Create a user
        user = User.objects.create_user(username="testuser", email="testuser@email.com", password="testpassword")
        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)

        # Request password reset
        url = reverse("accounts:password_reset")
        data = {"email": user.email}
        response = self.client.post(url, data, format="json")
        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(response.status_code, 200)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Password reset e-mail has been sent.")

    def test_email_verification_is_successful(self):
        """Test that email verification works properly"""
        # Clear any existing emails
        # mail.outbox.clear()

        # Create a user account
        data = {
            "email": "testuser345@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.registration_url, data, format="json")
        self.assertEqual(response.status_code, 201)

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to[0], data["email"])
        self.assertIn("Confirm", email.subject)

        # Check that the email contains a verification link
        email_body = email.body
        self.assertIn("confirm-email", email_body)

        # Extract the verification key from the email
        # The key format is typically in the URL: /confirm-email/key/

        key_match = re.search(r"/confirm-email/([^/]+)/", email_body)
        self.assertIsNotNone(key_match, "Verification key not found in email")
        verification_key = key_match.group(1)

        # Test that the user can verify their email
        confirm_url = f"/api/accounts/confirm-email/{verification_key}/"
        response = self.client.post(confirm_url)

        # The response should be successful (usually redirects or returns success)
        self.assertIn(response.status_code, [200, 302, 201])

        # Check that the email is now verified in the database
        email_address = EmailAddress.objects.get(email=data["email"])
        self.assertTrue(email_address.verified)

        # Verify the user can now log in (since email is verified)
        login_url = reverse("accounts:login")
        login_data = {
            "email": data["email"],
            "password": data["password1"],
        }

        response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_email_verification_invalid_key(self):
        """Test that invalid verification keys are rejected"""
        # Try to verify with an invalid key
        invalid_key = "invalid-key-12345"
        confirm_url = f"/api/accounts/confirm-email/{invalid_key}/"

        response = self.client.post(confirm_url)

        # Should return an error (404)
        self.assertEqual(response.status_code, 404)

    def test_email_verification_already_verified_email_returns_404(self):
        """Test that already verified emails can't be verified again"""
        # Clear any existing emails
        mail.outbox.clear()

        # Create a user account
        data = {
            "email": "testuser2@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.registration_url, data, format="json")
        self.assertEqual(response.status_code, 201)

        # Get the verification email
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        # Extract the verification key
        key_match = re.search(r"/confirm-email/([^/]+)/", email.body)
        verification_key = key_match.group(1)

        # Verify the email first time
        confirm_url = f"/api/accounts/confirm-email/{verification_key}/"
        response = self.client.post(confirm_url)
        self.assertIn(response.status_code, [200, 302, 201])

        # Try to verify the same email again
        response = self.client.post(confirm_url)

        # Should handle gracefully (might return error or success message)
        # The exact behavior depends on allauth implementation
        self.assertEqual(response.status_code, 404)

    def test_email_verification_email_content(self):
        """Test that verification emails contain proper content"""
        # Clear any existing emails
        # mail.outbox.clear()

        # Create a user account
        data = {
            "email": "testuser3@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.registration_url, data, format="json")
        self.assertEqual(response.status_code, 201)

        # Check email content
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        # Verify email properties
        self.assertEqual(email.to[0], data["email"])
        self.assertIn("Confirm", email.subject)

        # Check that email body contains necessary information
        email_body = email.body
        self.assertIn("confirm-email", email_body)
        self.assertIn(
            "You're receiving this email because user testuser3 "
            "has given your email address to register an account on testserver",
            email_body,
        )

        # Check that the verification URL is properly formatted
        url_pattern = r"/api/accounts/confirm-email/[^/\s]+/"
        self.assertIsNotNone(
            re.search(url_pattern, email_body), "Properly formatted verification URL not found in email"
        )
