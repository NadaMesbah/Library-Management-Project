from django.db import models
import uuid
from datetime import datetime, timedelta
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    CNI = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")
    departement = models.CharField(max_length=200, blank=True, null=True)
    filiere = models.CharField(max_length=200, blank=True, null=True)
    CNE = models.CharField(max_length=200, blank=True, null=True)
    semestre = models.CharField(max_length=200, blank=True, null=True)
    sexe = models.CharField(max_length=200, blank=True, null=True)
    phonenumber = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    def __str__(self):
        return str(self.CNE)

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url
    
class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
        
class UserEmail(models.Model):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.email


class Reclamation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    nom = models.CharField(max_length=200,default=False, blank=True)
    email = models.EmailField(default=False, blank=True)
    sujet = models.TextField(default=False, blank=True)
    message = models.TextField(default=False, blank=True)
    ouvrage = models.ForeignKey('ouvrages.Ouvrage', on_delete=models.SET_NULL, null=True)
    
    def _str_(self):
        return f'Reservation {self.nom}'
