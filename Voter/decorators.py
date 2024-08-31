from functools import wraps
from django.http import HttpResponseForbidden

def conditional_decorator(condition_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0]  # Assuming the first argument is always request
            if condition_func(request):
                return func(*args, **kwargs)
            else:
                return HttpResponseForbidden("You are not authorized to view this page.")
        return wrapper
    return decorator