from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import login


def homepage(request):
    return render(request, './templates/main.html', {'section': 'homepage'})

def register(request):
    page = 'register'
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            user = user_form.save(commit=False)
            # Set the chosen password
            user.set_password(
                user_form.cleaned_data['password1'])
            # Save the user object
            user.save()
            messages.success(request, 'User account was created!')
            return render(request, 'adherants/register_done.html', {'new_user':user})  # Redirect to the login after successful regestration
    else:
        messages.success(
            request, 'An error has occurred during registration')
    
    user_form = RegisterForm()
    return render(request, 'adherants/login_register.html', {'user_form': user_form, 'page' : page})

def login(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Username OR password is incorrect')
    return render(request, 'adherants/login_register.html', {'page' : page})

def password_reset(request):
    return render(request, 'adherants/password_reset.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('homepage')

@login_required
def profile(request):
    user = request.user  # Retrieve the current user

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        user_form = UserForm(request.POST, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user  # Associate the profile with the current user
            profile.save()
            user_form.save()
            return redirect('profile')
    else:
        # Check if the user has a profile instance, create one if not
        if hasattr(user, 'profile'):
            profile_form = ProfileForm(instance=user.profile)
        else:
            profile_form = ProfileForm()

        user_form = UserForm(instance=user)

    context = {
        'user': user,
        'profile_form': profile_form,
        'user_form': user_form,
    }
    return render(request, 'adherants/profile.html', context)
