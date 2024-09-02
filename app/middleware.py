from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of paths that don't require login
        exempt_urls = [reverse('login')]  # Add other exempt paths as needed

        # Check if user is authenticated or the request path is exempt
        if not request.user.is_authenticated and request.path not in exempt_urls:
            # Redirect to the login page
            return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        return response


class SimpleLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')
        response = self.get_response(request)
        return response
