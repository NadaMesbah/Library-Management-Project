from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login/", views.login, name="login"),
    
    # User registration : 
    path("register/", views.register, name="register"),
    
    path("logout/", views.logout, name="logout"),

    # Django's built-in password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='adherants/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='adherants/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='adherants/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='adherants/password_reset_complete.html'), name='password_reset_complete'),
    
    path('edit-profile/', login_required(views.editProfile), name="edit-profile"),
    path('profile/', login_required(views.profile), name="profile"),
    
    path('contact/', login_required(views.contact), name="contact"),
    
    path('contact_succes/',views.contact_succes, name='contact_succes'),
    path('collect_email/',views.collect_email, name='collect_email'),
    
    path('user-profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('profiles/', views.profiles, name='profiles'),
    
    path('inbox/', login_required(views.inbox), name="inbox"),
    path('message/<str:pk>/', login_required(views.viewMessage), name="message"),
    path('create-message/<str:pk>/',login_required( views.createMessage), name="create-message"),

    ]



