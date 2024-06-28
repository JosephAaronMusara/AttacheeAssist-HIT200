# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class UserRoleRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return response
           # elif request.user.role == 'employer' and not request.path.startswith(reverse('jobapp:dashboard')):
            #    return redirect(reverse('jobapp:dashboard'))
            elif request.user.role == 'employee' and not request.path.startswith(reverse('jobapp:home')):
                return redirect(reverse('jobapp:home')) 
            elif request.user.role == 'coordinator' and not request.path.startswith(reverse('jobapp:coordinator')):
                return redirect(reverse('jobapp:coordinator'))
            elif request.user.role == 'supervisor' and not request.path.startswith(reverse('jobapp:dashboard')):
                return redirect(reverse('jobapp:dashboard'))
        return response
