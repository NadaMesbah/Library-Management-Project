from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from .utils import searchProfiles, paginateProfiles
from django.urls import conf
from ouvrages.models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Profile, Message, Reclamation, UserEmail
from .forms import LoginForm, ProfileForm, UserForm, RegisterForm, UserEmailForm, ContactForm, MessageForm

def homepage(request):
    return render(request, './templates/main.html', {'section': 'homepage'})

def handling_404(request, exception):
    return render(request, '../templates/404.html',{})

def handling_500(request):
    return render(request, '../templates/500.html',{})

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
            return render(request, 'adherants/register_done.html', {'new_user':user})  # Redirect to the login after successful registration
        else:
            messages.error(request, 'An error has occurred during registration')  # Display error message if form validation fails
    else:
        user_form = RegisterForm()
    return render(request, 'adherants/login_register.html', {'user_form':user_form,'page': page})
# def register(request):
#     page = 'register'
#     form = CustomUserCreationForm()

#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()

#             messages.success(request, 'User account was created!')

#             login(request, user)
#             return redirect('edit-account')

#         else:
#             messages.success(
#                 request, 'An error has occurred during registration')

#     context = {'page': page, 'form': form}
#     return render(request, 'adherants/register_done.html', context)

# def login(request):
#     page = 'login'

#     if request.user.is_authenticated:
#         return redirect('profiles')

#     if request.method == 'POST':
#         username = request.POST['username'].lower()
#         password = request.POST['password']

#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, 'Username does not exist')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect(request.GET['next'] if 'next' in request.GET else 'account')

#         else:
#             messages.error(request, 'Username OR password is incorrect')

#     return render(request, 'adherants/login_register.html')


def logout(request):
    auth_logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('homepage')

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

        # if user is not None:
        #     login(request, user)
        #     return redirect(request.GET['next'] if 'next' in request.GET else 'profile')
        if user is not None:
            auth_login(request, user)  # Rename login function call to auth_login
            return redirect(request.GET.get('next', 'profile'))
        else:
            messages.error(request, 'Username OR password is incorrect')
    return render(request, 'adherants/login_register.html', {'page' : page})

def password_reset(request):
    return render(request, 'adherants/password_reset.html')


# @login_required
# def profile(request):
#     profile = request.user.profile
#     context = {
#         'profile': profile,
#     }
#     return render(request, 'adherants/profile.html', context)

@login_required
def profile(request):
    profile = request.user.profile
    # user = request.user  # Retrieve the current user

    # if request.method == 'POST':
    #     profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
    #     user_form = UserForm(request.POST, instance=user)
    #     if profile_form.is_valid() and user_form.is_valid():
    #         profile = profile_form.save(commit=False)
    #         profile.user = user  # Associate the profile with the current user
    #         profile.save()
    #         user_form.save()
    #         return redirect('profile')
    # else:
    #     # Check if the user has a profile instance, create one if not
    #     if hasattr(user, 'profile'):
    #         profile_form = ProfileForm(instance=user.profile)
    #     else:
    #         profile_form = ProfileForm()

    #     user_form = UserForm(instance=user)
    #     profile = Profile.objects.get(user=request.user)
        
    context = {
        # 'user': user,
        # 'profile_form': profile_form,
        # 'user_form': user_form,
        'profile' : profile,
    }
    return render(request, 'adherants/profile.html', context)

# @login_required
# def editProfile(request):
#     profile = request.user.profile
#     form = ProfileForm(instance=profile)

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()

#             return redirect('profile')

#     context = {'form': form}
#     return render(request, 'adherants/profile.html', context)


# @login_required(login_url='login')
# def userProfile(request):
#     profile = request.user.profile
#     context = {'profile': profile}
#     return render(request, 'adherants/profile.html', context)


@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('profile')

    context = {'form': form}
    return render(request, 'adherants/profile_form.html', context)

# #li shuia logic
# def collect_email(request):
#     if request.method == 'POST':
#         form = UserEmailForm(request.POST)
#         if form.is_valid():
#             user_email = form.save()

#             # Envoi de l'email
#             send_mail(
#                 'Merci pour votre abonnement',
#                 'Vous êtes maintenant abonné à notre newsletter.',
#                 'info@company.com',
#                 [user_email.email],  # Remplacez ceci par le champ email de votre modèle
#                 fail_silently=False,
#             )

#             messages.success(request, 'Merci pour votre abonnement! Vous êtes maintenant abonné à notre newsletter.')
#             return render(request, 'ouvrages/index.html')
#         else:
#             messages.error(request, 'Une erreur est survenue. Veuillez réessayer.')
#             return render(request, 'ouvrages/index.html')

#     else:
#         form = UserEmailForm()
#         return render(request, 'ouvrages/index.html', {'form': form})

def profiles(request):  
    profiles, search_query = searchProfiles(request)
    
    profiles = profiles.filter(
        user__is_staff=False
    )
    #custom_range, profiles = paginateProfiles(request, profiles, 1)
    context = {'profiles': profiles, 'search_query': search_query}
            #    'custom_range': custom_range
    return render(request, 'adherants/profiles.html', context)

def userProfile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    reservations = Reservation.objects.filter(owner=profile)

    context = {
        'profile': profile,
        'reservations': reservations
    }
    return render(request, 'adherants/user-profile.html', context)


def collect_email(request):
    keyword = request.GET.get('keyword') if request.GET.get('keyword') else ''
    ouvrages = Ouvrage.objects.filter(
        Q(categories__name__icontains=keyword) |
        Q(titre__icontains=keyword) |
        Q(description__icontains=keyword) |
        Q(auteurs__nomComplet__icontains=keyword)
    )
    #categories = ouvrage.categories.all() ==> ouvrage is an instance of Ouvrage
    #ouvrages = Ouvrage.objects.all()
    categories = Categorie.objects.all()
    ouvrage_count = ouvrages.count()
    best_ouvrage = Ouvrage.objects.exclude(vote_total=0).order_by('-vote_ratio').first()
    newest_ouvrage = Ouvrage.objects.order_by('-date_achat').first()
    recommended_ouvrages = Ouvrage.objects.filter(recommended=True)
    context = {'ouvrages': ouvrages, 'categories': categories,
               'ouvrage_count': ouvrage_count, 'best_ouvrage' : best_ouvrage, 
               'newest_ouvrage': newest_ouvrage , 'recommanded_ouvrages' : recommended_ouvrages}
    if request.method == 'POST':
        email = request.POST.get('email')
        form = UserEmailForm(request.POST)
        if UserEmail.objects.filter(email=email).exists():
            messages.info(request, 'Vous êtes déjà abonné à notre newsletter.')
            return render(request, 'ouvrages/index.html', context)
        if form.is_valid():
            user_email = form.save()

            # Envoi de l'email
            send_mail(
                'Merci pour votre abonnement',
                'Vous êtes maintenant abonné à notre newsletter.',
                'info@company.com',
                [user_email.email],  # Remplacez ceci par le champ email de votre modèle
                fail_silently=False,
            )

            messages.success(request, 'Merci pour votre abonnement! Vous êtes maintenant abonné à notre newsletter.')
            return render(request, 'ouvrages/index.html', context)
        else:
            messages.error(request, 'Une erreur est survenue. Veuillez réessayer.')
            return render(request, 'ouvrages/index.html', context)

    else:
        form = UserEmailForm()
        return render(request, 'ouvrages/index.html', context, {'form': form})
    
# def collect_email(request):
#     if request.method == 'POST':
#         form = UserEmailForm(request.POST)
#         if form.is_valid():
#             user_email = form.save()

#             # Envoi de l'email
#             send_mail(
#                 'Merci pour votre abonnement',
#                 'Vous êtes maintenant abonné à notre newsletter.',
#                 'info@company.com',
#                 [user_email.email],  # Remplacez ceci par le champ email de votre modèle
#                 fail_silently=False,
#             )
#             messages.success(request, 'Merci pour votre abonnement! Vous êtes maintenant abonné à notre newsletter.')
#             return render(request, 'ouvrages/index.html')
#         else:
#             messages.error(request, 'Une erreur est survenue. Veuillez réessayer.')
#             return render(request, 'ouvrages/index.html', {'form': form})  # Return the form in case of validation errors
#     else:
#         form = UserEmailForm()
#         return render(request, 'ouvrages/index.html', {'form': form})
    
# def collect_email(request):
#     if request.method == 'POST':
#         form = UserEmailForm(request.POST)
#         if form.is_valid():
#             user_email = form.save()

#             # Envoi de l'email
#             send_mail(
#                 'Merci pour votre abonnement',
#                 'Vous êtes maintenant abonné à notre newsletter.',
#                 'info@company.com',
#                 [user_email.email],  # Remplacez ceci par le champ email de votre modèle
#                 fail_silently=False,
#             )
#             messages.success(request, 'Merci pour votre abonnement! Vous êtes maintenant abonné à notre newsletter.')
#             return render(request, 'ouvrages/index.html')
#         else:
#             messages.error(request, 'Une erreur est survenue. Veuillez réessayer.')
#     else:
#         form = UserEmailForm()
#         return render(request, 'ouvrages/index.html', {'form': form})
    
       

def password_reset(request):
    return render(request, 'adherants/password_reset.html')

def send_confirmation_email(email, name):
    subject = 'Confirmation de réception de votre réclamation'
    message = 'Cher {},\n\nNous avons bien reçu votre réclamation et nous vous répondrons dans les plus brefs délais.\n\nCordialement,\nL\'équipe de support'.format(name)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    
def contact(request):
    if request.method == 'POST':
        sujet = request.POST.get('subject')
        nom = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if nom and email and sujet and message:  # Vérifiez que toutes les valeurs sont non nulles
            # Créer une nouvelle réclamation
            reclamation = Reclamation(nom=nom, email=email, sujet=sujet,message=message)
            reclamation.save()

            # Envoyer l'email de confirmation
            try:
                send_confirmation_email(email, nom)
                messages.success(request, 'Votre réclamation a été envoyé à notre support avec succes.')
                return render(request, 'adherants/contact.html')
            except Exception as e:
                return render(request, 'adherants/contact.html', {'error': str(e)})
        else:
            # Gérer le cas où une ou plusieurs valeurs sont nulles
            # Vous pouvez par exemple renvoyer le formulaire avec un message d'erreur
            return render(request, 'adherants/contact.html', {'error': 'Tous les champs sont obligatoires.'})
    else: 
        return render(request, 'adherants/contact.html')


def contact_succes(request):
    return render(request, 'adherants/contact_success.html')


def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'adherants/inbox.html', context)


def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'adherants/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.username
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'adherants/message_form.html', context)

