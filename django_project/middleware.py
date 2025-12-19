import re

from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware


class CustomCsrfViewMiddleware(CsrfViewMiddleware):
    def process_request(self, request):
        # Check if the URL should be CSRF exempted
        if hasattr(settings, "CSRF_EXEMPT_URLS"):
            for pattern in settings.CSRF_EXEMPT_URLS:
                if re.match(pattern, request.path):
                    # Set a flag to skip CSRF validation for this request
                    request._dont_enforce_csrf_checks = True
                    return None
        return super().process_request(request)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Check if this URL should be exempted from CSRF
        if hasattr(settings, "CSRF_EXEMPT_URLS"):
            for pattern in settings.CSRF_EXEMPT_URLS:
                if re.match(pattern, request.path):
                    return None

        # If CSRF checks are disabled for this request, skip them
        if getattr(request, "_dont_enforce_csrf_checks", False):
            return None

        return super().process_view(request, callback, callback_args, callback_kwargs)
