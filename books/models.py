from django.db import models
import uuid
from datetime import datetime, timedelta
from adherant.models import Adherant 
from bibliothecaire.models import Bibliothecaire
# Create your models here.

class Ouvrage(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='img', blank=True, null=True)
    auteur = models.CharField(max_length=50)
    description = models.TextField()
    categories = models.ManyToManyField(Categorie, related_name='ouvrages')
    ouvrages_recommendes = models.BooleanField(default=False)
    num_exemplaires = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.titre} by {self.auteur}"

    class Meta:
        verbose_name_plural = "Ouvrages"
    
class Categorie(models.Model):
    nomC = models.CharField('Categorie', max_length=50)
    description = models.TextField('Description')

    def __str__(self):
        return self.nomC

class Rayon(models.Model):
    nomR = models.CharField('Rayon', max_length=50)
    localisation = models.CharField('Localisation', max_length=100)
    capacity = models.PositiveIntegerField('Capacity')

    def __str__(self):
        return self.nomR
    
class Exemplaire(models.Model):
    
    HORS_PRET = 'HP'
    DISPONIBLE = 'DI'
    PERDU = 'PE'
    RETIRE = 'RE'

    ETAT_CHOICES = [
        (HORS_PRET, 'Hors Prêt'),
        (DISPONIBLE, 'Disponible'),
        (PERDU, 'Perdu'),
        (RETIRE, 'Retiré de la Base'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ouvrage = models.ForeignKey(Ouvrage, on_delete=models.CASCADE, related_name='exemplaires', verbose_name='Ouvrage')
    etat = models.CharField(max_length=2, choices=ETAT_CHOICES, default=HORS_PRET, verbose_name='État')

    class Meta:
        verbose_name = 'Exemplaire'
        verbose_name_plural = 'Exemplaires'

    def __str__(self):
        return f"Exemplaire de l'ouvrage {self.ouvrage.titre}"
    
    def save(self, *args, **kwargs):
        # Increment the number of exemplaires for the related Ouvrage
        self.ouvrage.num_exemplaires += 1
        self.ouvrage.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Decrement the number of exemplaires for the related Ouvrage
        self.ouvrage.num_exemplaires -= 1
        self.ouvrage.save()
        super().delete(*args, **kwargs)

def get_expiry():
    return datetime.today() + timedelta(days=15)

class Emprunt(models.Model):
    emprunteur = models.ForeignKey(Adherant, on_delete=models.CASCADE, verbose_name='Emprunteur')
    exemplaire = models.ForeignKey(Exemplaire, on_delete=models.CASCADE, verbose_name='Exemplaire')
    date_emprunt = models.DateField(auto_now=True, verbose_name='Date d\'Emprunt')
    date_retour = models.DateField(default=get_expiry, verbose_name='Date de Retour Prévue')
    rendu = models.BooleanField(default=False, verbose_name='Rendu')
    bibliothecaire = models.ForeignKey('Bibliothecaire', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Emprunt'
        verbose_name_plural = 'Emprunts'

    def __str__(self):
        return f"{self.emprunteur.username}"

    def save(self, *args, **kwargs):
        if self.rendu:
            # Update the num_exemplaires field of the related Ouvrage when the book is returned
            self.exemplaire.ouvrage.num_exemplaires += 1
            self.exemplaire.ouvrage.save()
        super().save(*args, **kwargs)
    
class Reservation(models.Model):
    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_demande = models.DateTimeField(auto_now_add=True)
    date_reservation = models.DateField()
    adherant = models.ForeignKey(Person, on_delete=models.CASCADE)
    exemplaire = models.ForeignKey(Exemplaire, on_delete=models.CASCADE)
    acceptee = models.BooleanField(default=False)
    bibliothecaire = models.ForeignKey('Bibliothecaire', on_delete=models.SET_NULL, null=True, blank=True)
