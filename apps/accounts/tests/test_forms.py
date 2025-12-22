from django.test import TestCase

from apps.accounts.forms import PhoneChangeForm


class PhoneChangeFormTests(TestCase):
    """Test cases for PhoneChangeForm"""

    def test_form_has_phone_field(self):
        """Test that PhoneChangeForm has a phone field"""
        form = PhoneChangeForm()
        self.assertIn("phone", form.fields)

    def test_form_phone_field_is_phone_number_field(self):
        """Test that phone field is a PhoneNumberField"""
        form = PhoneChangeForm()
        from phonenumber_field.formfields import PhoneNumberField

        self.assertIsInstance(form.fields["phone"], PhoneNumberField)

    def test_form_phone_field_is_not_required(self):
        """Test that phone field is not required"""
        form = PhoneChangeForm()
        self.assertFalse(form.fields["phone"].required)

    def test_form_valid_with_valid_phone(self):
        """Test that form is valid with a valid phone number"""
        form = PhoneChangeForm(data={"phone": "+256756789580"})
        self.assertTrue(form.is_valid())
        self.assertNotIn("phone", form.errors)

    def test_form_valid_with_empty_phone(self):
        """Test that form is valid with empty phone (since it's not required)"""
        form = PhoneChangeForm(data={"phone": ""})
        self.assertTrue(form.is_valid())
        self.assertNotIn("phone", form.errors)

    def test_form_valid_with_none_phone(self):
        """Test that form is valid with None phone"""
        form = PhoneChangeForm(data={})
        self.assertTrue(form.is_valid())
        self.assertNotIn("phone", form.errors)

    def test_form_invalid_with_invalid_phone(self):
        """Test that form is invalid with an invalid phone number"""
        form = PhoneChangeForm(data={"phone": "123"})
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_form_cleaned_data_with_valid_phone(self):
        """Test that form cleaned_data contains phone number"""
        form = PhoneChangeForm(data={"phone": "+256756789580"})
        print(form.errors)
        self.assertTrue(form.is_valid())
        phone = form.cleaned_data.get("phone")
        # PhoneNumberField returns a PhoneNumber object or string representation
        self.assertIsNotNone(phone)
        self.assertEqual(str(phone), "+256756789580")

    def test_form_cleaned_data_with_empty_phone(self):
        """Test that form cleaned_data contains empty string or None for empty phone"""
        form = PhoneChangeForm(data={"phone": ""})
        self.assertTrue(form.is_valid())
        phone = form.cleaned_data.get("phone")
        # PhoneNumberField returns empty string or None when empty
        self.assertTrue(phone is None or phone == "")

    def test_form_phone_field_has_help_text(self):
        """Test that phone field has help text"""
        form = PhoneChangeForm()
        self.assertTrue(form.fields["phone"].help_text)

    def test_form_phone_field_has_label(self):
        """Test that phone field has a label"""
        form = PhoneChangeForm()
        self.assertTrue(form.fields["phone"].label)
