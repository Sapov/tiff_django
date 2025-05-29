# middleware.py
from django.shortcuts import redirect


class RoleRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.path == '/profile/':
                if request.user.role == 'CUSTOMER_RETAIL':
                    return redirect('account:dashboard')
                elif request.user.role == 'DESIGNER':
                    return redirect('designs:design_list')

        return response