from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile
from ouvrages.models import *

from django.core.mail import send_mail
from django.conf import settings

# @receiver(post_save, sender=Profile)


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            prenom=user.first_name,
            nom=user.last_name,
        )

        subject = 'Welcome to Bibliotheque'
        message = 'We are glad you are here!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.prenom
        user.last_name = profile.nom
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

def envoyer_email_nouvel_ouvrage(instance_id):
    instance = Ouvrage.objects.get(id=instance_id)
    sujet = f'Nouvel ouvrage ajouté : {instance.titre}'
    emails = UserEmail.objects.values_list('email', flat=True)
    contexte = {
        'titre': instance.titre,
        'auteurs': instance.auteurs,
        'categories': instance.categories,
        'description': instance.description,
        'lien_details': f"http://localhost:8000/single-ouvrage/{instance.id}"  # Lien vers la page de détails de l'ouvrage
    }
    message = render_to_string('ouvrages/nouvel_ouvrage_email.html', contexte)
    send_mail(sujet, message, 'votre_email@example.com', emails)

@receiver(post_save, sender=Ouvrage)
def post_save_ouvrage(sender, instance, created, **kwargs):
    if created:
        envoyer_email_nouvel_ouvrage(instance.id)
        
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
