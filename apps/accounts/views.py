from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from apps.accounts.forms import PhoneChangeForm
from apps.users.models import Profile


@method_decorator(login_required, name="dispatch")
class ProfileView(TemplateView):
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        # Get profile if it exists
        if hasattr(user, "profile"):
            context["profile"] = user.profile
        return context


@method_decorator(login_required, name="dispatch")
class PhoneChangeView(FormView):
    template_name = "account/phone_change.html"
    form_class = PhoneChangeForm
    success_url = "/accounts/profile/"

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        if hasattr(user, "profile") and user.profile.phone:
            initial["phone"] = user.profile.phone
        return initial

    def form_valid(self, form):
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = form.cleaned_data.get("phone")
        profile.save()
        messages.success(self.request, "Phone number updated successfully.")
        return redirect("account_profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        # Get profile if it exists
        if hasattr(user, "profile"):
            context["profile"] = user.profile
            context["phone"] = user.profile.phone
            context["phone_verified"] = True  # Simplified - you can add verification logic later
        else:
            context["phone"] = None
            context["phone_verified"] = False
        return context
