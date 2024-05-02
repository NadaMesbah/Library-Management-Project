from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

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
    
    path('edit-profile/', views.editProfile, name="edit-profile"),
    path("profile/", views.profile, name="profile"),
]



