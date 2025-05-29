# middleware.py
from django.shortcuts import redirect


class RoleRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.path == '/profile/':
                if request.user.role == 'DESIGNER':
                    return redirect('designs:design_list')
                else:
                    return redirect('account:dashboard')

        return response




# class RoleRedirectMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.role_redirects = {
#             'CLIENT': 'client_dashboard',
#             'DESIGNER': 'designer_dashboard',
#             'MANAGER': 'manager_dashboard',
#         }
#
#     def __call__(self, request):
#         # Игнорируем AJAX-запросы и API-эндпоинты
#         if (request.path.startswith('/api/') or
#                 request.headers.get('x-requested-with') == 'XMLHttpRequest'):
#             return self.get_response(request)
#
#         if request.user.is_authenticated and request.path == '/profile/':
#             if hasattr(request.user, 'role'):
#                 role = request.user.role
#                 if role in self.role_redirects:
#                     return redirect(self.role_redirects[role])
#
#         return self.get_response(request)