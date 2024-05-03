from django.contrib import admin
from .models import Profile, Message, Reclamation, UserEmail

# Register your models here.
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Reclamation)
admin.site.register(UserEmail)