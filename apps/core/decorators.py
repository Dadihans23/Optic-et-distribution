from functools import wraps
from django.shortcuts import redirect


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('uid'):
            return redirect('authentication:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('uid'):
            return redirect('authentication:login')
        if request.session.get('role') != 'admin':
            return redirect('dashboard:index')
        return view_func(request, *args, **kwargs)
    return wrapper
