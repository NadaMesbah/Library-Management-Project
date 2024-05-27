from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.deletion import CASCADE
from adherants.models import Profile

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
        return f"{self.nomComplet}"
    
class Ouvrage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    titre = models.CharField(max_length=200)
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
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'titre']
    
    def save(self, *args, **kwargs):
        # Automatically set recommended to True if vote_ratio is above 80%
        if self.vote_ratio > 80:
            self.recommended = True
        else:
            self.recommended = False
        super(Ouvrage, self).save(*args, **kwargs)
    
    def update_exemplaires_total(self):
        self.exemplaires_total = self.exemplaire_set.count()
        self.save()
        
    def count_available_exemplaires(self):
        return self.exemplaire_set.filter(etat='DISPONIBLE').count()
    
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()
        
class Review(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    ouvrage = models.ForeignKey('Ouvrage', on_delete=models.CASCADE)
    VOTE_TYPE =(
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    #choices is gonna be a drop down list and the user can select from it
    rating = models.PositiveIntegerField(default=0)  # Add this line
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.value

class Rayon(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    localisation = models.CharField('Localisation', max_length=200)

    def __str__(self):
        return self.localisation
    
class Exemplaire(models.Model):
    
    ETAT_CHOICES = [
        ('HORS_PRET', 'Hors Prêt'),
        ('DISPONIBLE', 'Disponible'),
        ('PERDU', 'Perdu'),
        ('RETIRE', 'Retiré'),
        ('A_ENLEVER', 'À enlever'),
    ]
    id = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)
    ouvrage = models.ForeignKey('Ouvrage', on_delete=models.CASCADE)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='DISPONIBLE')
    reserve = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # If id is not set, it will be handled in the view
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Exemplaire {self.id} de l'ouvrage {self.ouvrage.titre}"
    
    class Meta:
        ordering = ['-created']
    

    
# @receiver(post_save, sender=Exemplaire)
# def update_ouvrage_on_exemplaire_save(sender, instance, created, **kwargs):
#     if created:
#         instance.ouvrage.exemplaires_total += 1
#         instance.ouvrage.save()

# @receiver(post_delete, sender=Exemplaire)
# def update_ouvrage_on_exemplaire_delete(sender, instance, **kwargs):
#     instance.ouvrage.exemplaires_total -= 1
#     instance.ouvrage.save()
# models.py

# models.py


class Emprunt(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    emprunteur = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='emprunts', null=True, blank=True)
    exemplaire = models.ForeignKey('Exemplaire', on_delete=models.CASCADE, related_name='emprunts')
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField(null=True, blank=True)
    rendu = models.BooleanField(default=False, blank=True)
    automatique = models.BooleanField(default=True)  # Champ pour identifier les emprunts automatiques
    confirmer = models.BooleanField(default=False)  # Champ pour indiquer si l'emprunt a été confirmé par le bibliothécaire

    @property
    def calculer_date_retour(self):
        return self.date_emprunt + timedelta(days=15)
    
    def save(self, *args, **kwargs):
        if self.rendu:
            if not self.pk or (self.pk and not Emprunt.objects.get(pk=self.pk).rendu):
                self.exemplaire.ouvrage.exemplaires_total += 1
                self.exemplaire.ouvrage.save()

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Emprunt de l'exemplaire {self.exemplaire.id} de la part de {self.emprunteur.username}"


# @receiver(post_save, sender=Emprunt)
# def update_exemplaire_on_emprunt_save(sender, instance, created, **kwargs):
#     if created:
#         instance.exemplaire.ouvrage.exemplaires_total -= 1
#         instance.exemplaire.ouvrage.save()

# @receiver(post_delete, sender=Emprunt)
# def update_exemplaire_on_emprunt_delete(sender, instance, **kwargs):
#     instance.exemplaire.ouvrage.exemplaires_total += 1
#     instance.exemplaire.ouvrage.save()

# class Emprunt(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
#     emprunteur = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
#     exemplaire = models.ForeignKey('Exemplaire', on_delete=models.CASCADE)
#     date_emprunt = models.DateTimeField(auto_now_add=True)
#     date_retour = models.DateTimeField(null=True, blank=True)
#     rendu = models.BooleanField(default=False)
#     destroyed = models.BooleanField(default=False)

#     @property
#     def calculer_date_retour(self):
#         return self.date_emprunt + timedelta(days=15)

#     def save(self, *args, **kwargs):
#         if self.rendu:
#             self.exemplaire.etat = 'DISPONIBLE'
#             self.exemplaire.ouvrage.exemplaires_total += 1
#             self.exemplaire.ouvrage.save()
#         elif self.destroyed:
#             self.exemplaire.etat = 'A_ENLEVER'
#         super().save(*args, **kwargs)

# @receiver(post_save, sender=Emprunt)
# def update_exemplaire_on_emprunt_save(sender, instance, created, **kwargs):
#     if not created:
#         previous_instance = Emprunt.objects.get(pk=instance.pk)
#         if instance.rendu and not previous_instance.rendu:
#             instance.exemplaire.etat = 'DISPONIBLE'
#             instance.exemplaire.ouvrage.exemplaires_total += 1
#             instance.exemplaire.ouvrage.save()
#         elif instance.destroyed and not previous_instance.destroyed:
#             instance.exemplaire.etat = 'A_ENLEVER'
#         instance.exemplaire.save()

# @receiver(post_delete, sender=Emprunt)
# def update_exemplaire_on_emprunt_delete(sender, instance, **kwargs):
#     if not instance.rendu and not instance.destroyed:
#         instance.exemplaire.etat = 'PERDU'
#         # Check if the Emprunt is older than one year
#         if instance.date_emprunt < timezone.now() - timedelta(days=365):
#             instance.exemplaire.delete()
#         else:
#             instance.exemplaire.save()

#exemple de creation d'un emprunt
# emprunt = Emprunt.objects.create(
#     exemplaire=your_exemplaire_instance,
#     date_retour=emprunt.calculate_return_date()  
# )

class Reservation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    date_demande =  models.DateTimeField(auto_now_add=True)
    date_reservation = models.DateTimeField()
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    ouvrage = models.ForeignKey('Ouvrage', on_delete=models.CASCADE, null=True)  # Lier à Ouvrage
    selected_copy = models.ForeignKey('Exemplaire', on_delete=models.CASCADE, null=True, blank=True)
    
    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    )
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_retour_prevue = models.DateField(null=True, blank=True)
    
    def can_be_converted_to_emprunt(self):
        today = datetime.now().date()
        return self.statut == 'acceptee' and self.date_reservation <= today

    
