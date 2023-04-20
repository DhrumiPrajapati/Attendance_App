from django.shortcuts import redirect
from django.urls import resolve

from Attendance.views import loginview

class PreventLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            view_func, args, kwargs = resolve(request.path)
            if view_func == loginview:
                return redirect('AttFormView') # Replace 'AttForm' with the name of your home view
        response = self.get_response(request)
        return response

# from django.shortcuts import redirect

# class PreventLoginRedirectMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated and request.path == 'loginview':
#             return redirect('AttForm') # Replace 'home' with the name of your home view
#         response = self.get_response(request)
#         return response