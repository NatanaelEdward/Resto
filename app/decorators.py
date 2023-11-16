from django.shortcuts import redirect

def role_required(allowed_roles=()):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if request.user.userprofile.role not in allowed_roles:
                return redirect('login_view')  # Redirect to the login page for unauthorized roles
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator