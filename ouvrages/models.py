from django.db import models

# Create your models here.
from django.db import models
import uuid
from datetime import datetime, timedelta
# Create your models here.

class Categorie(models.Model):
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name

class Auteur(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    MONSIEUR = 'M'
    MADAME = 'MME' 
    TITLE_CHOICES = [
    (MONSIEUR, 'M.'),
    (MADAME, 'Mme.'),
    ]
    nomComplet = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} {self.nomComplet}"
    
class Ouvrage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    titre = models.CharField(max_length=200)
    #cover_image = models.ImageField(upload_to='img', blank=True, null=True)
    auteurs = models.ManyToManyField('Auteur', blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    description = models.TextField(blank=True)
    categories = models.ManyToManyField('Categorie', blank=True)
    recommended = models.BooleanField(default=False, blank=True)
    exemplaires_total = models.IntegerField(default=0, null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    #vote ratio to know the percentage of votes (positive or negative)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    date_achat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
    
class Review(models.Model):
    #adherant
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    ouvrage = models.ForeignKey('Ouvrage', on_delete=models.CASCADE)
    VOTE_TYPE =(
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    #choices is gonna be a drop down list and the user can select from it
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.value

class Rayon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    localisation = models.CharField('Localisation', max_length=200)

    def __str__(self):
        return self.localisation
    
class Exemplaire(models.Model):
    HORS_PRET = 'HP'
    DISPONIBLE = 'DI'
    PERDU = 'PE'
    RETIRE = 'RE'

    ETAT_CHOICES = [
        (HORS_PRET, 'Hors Prêt'),
        (DISPONIBLE, 'Disponible'),
        (PERDU, 'Perdu'),
        (RETIRE, 'Retiré'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ouvrage = models.ForeignKey('Ouvrage', on_delete=models.CASCADE)
    etat = models.CharField(max_length=2, choices=ETAT_CHOICES, default=HORS_PRET)

    def __str__(self):
        return f"Exemplaire de l'ouvrage {self.ouvrage.titre}"
    
    def save(self, *args, **kwargs):
        # Increment the number of exemplaires for the related Ouvrage
        self.ouvrage.exemplaires_total += 1
        self.ouvrage.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Decrement the number of exemplaires for the related Ouvrage
        self.ouvrage.exemplaires_total -= 1
        self.ouvrage.save()
        super().delete(*args, **kwargs)

class Emprunt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #emprunteur (Adherant)
    exemplaire = models.ForeignKey('Exemplaire', on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField()
    rendu = models.BooleanField(default=False)

    @property
    def calculer_date_retour(self):
        return self.date_emprunt + timedelta(days=15)
    
    def save(self, *args, **kwargs):
        if self.rendu:
            # Update the exemplaires_total field of the related Ouvrage when the book is returned
            self.exemplaire.ouvrage.exemplaires_total += 1
            self.exemplaire.ouvrage.save()
        super().save(*args, **kwargs)

#exemple de creation d'un emprunt
# emprunt = Emprunt.objects.create(
#     exemplaire=your_exemplaire_instance,
#     date_retour=emprunt.calculate_return_date()  
# )
class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_demande =  models.DateTimeField(auto_now_add=True)
    date_reservation = models.DateTimeField()
    #Adherant
    exemplaire = models.ForeignKey('Exemplaire', on_delete=models.CASCADE)
    acceptee = models.BooleanField(default=False)

