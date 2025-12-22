from django import forms
from phonenumber_field.formfields import PhoneNumberField


class PhoneChangeForm(forms.Form):
    phone = PhoneNumberField(
        required=False,
        label="Phone Number",
        help_text="Enter your phone number with country code",
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors",
                "type": "tel",
                "placeholder": "+1234567890",
            }
        ),
    )

