from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.shortcuts import redirect

def anonymous_required(function=None, redirect_url=None):
    """
    Decorator for views that checks that the user is not logged in.
    """
    if not redirect_url:
        redirect_url = reverse_lazy('homepage')  # Replace 'home' with the URL name of your home page or any other URL

    actual_decorator = user_passes_test(
        lambda user: not user.is_authenticated,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
