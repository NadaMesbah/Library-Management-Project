from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from django.utils.crypto import get_random_string
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms


from django.http import JsonResponse
from .utils import searchOuvrages, searchExemplaires, paginateOuvrages, paginateExemplaires, paginateReviews
from .models import *

class OuvrageForm(ModelForm):
    class Meta:
        model = Ouvrage
        fields = ['titre','featured_image', 'auteurs', 'description', 'categories', 'exemplaires_total']
        #fields = '__all__'
        widgets = {
            'categories': forms.SelectMultiple(),
            'auteurs': forms.SelectMultiple(),  # Change here
        }
    def __init__(self, *args, **kwargs):
        super(OuvrageForm, self).__init__(*args, **kwargs)
        self.fields['titre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ajouter un titre'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ajouter une description', 'style': 'border-radius: 30px'})
        self.fields['exemplaires_total'].widget.attrs.update({'class': 'form-control'})
        self.fields['featured_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['auteurs'].widget.attrs.update({'class': 'form-control', 'style': 'border-radius: 30px'})
        self.fields['categories'].widget.attrs.update({'class': 'form-control', 'style': 'border-radius: 30px'})

# class ExemplaireForm(ModelForm):
#     quantite = forms.IntegerField(label='Quantité')
#     class Meta:
#         model = Exemplaire
#         fields = ['ouvrage', 'etat', 'emprunte', 'reserve']
        
#     def __init__(self, *args, **kwargs):
#         super(ExemplaireForm, self).__init__(*args, **kwargs)
#         self.fields['ouvrage'].widget.attrs.update({'class': 'form-control'})
#         self.fields['etat'].widget.attrs.update({'class': 'form-control'}) 
      
class ExemplaireForm(forms.ModelForm):
    quantite = forms.IntegerField(label='Quantité', required=False) 
    class Meta:
        model = Exemplaire
        fields = ['ouvrage', 'etat', 'reserve']


    def __init__(self, *args, **kwargs):
        super(ExemplaireForm, self).__init__(*args, **kwargs)
        self.fields['ouvrage'].widget.attrs.update({'class': 'form-control'})
        self.fields['etat'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['reserve'].widget = forms.CheckboxInput()
        self.fields['quantite'].widget.attrs.update({'class': 'form-control'})
       
    def generate_unique_id(self):
        potential_id = f"FSM{get_random_string(length=4)}"
        while Exemplaire.objects.filter(id=potential_id).exists():
           
            potential_id = f"FSM{get_random_string(length=4)}"
       
        return potential_id

    @transaction.atomic
    def save(self, commit=True):
        quantite = self.cleaned_data.pop('quantite', 1)
        ouvrage = self.cleaned_data.get('ouvrage')
        exemplaires = []

        for _ in range(quantite):
            exemplaire = Exemplaire(**self.cleaned_data)
            exemplaire.id = self.generate_unique_id()
            exemplaires.append(exemplaire)

        Exemplaire.objects.bulk_create(exemplaires)

        # Update the exemplaires_total field
        ouvrage.exemplaires_total = Exemplaire.objects.filter(ouvrage=ouvrage).count()
        ouvrage.save()

        return exemplaires     
            
# class ExemplaireForm(forms.ModelForm):
#     quantite = forms.IntegerField(label='Quantité', required=False)  # Make it not required
    
#     class Meta:
#         model = Exemplaire
#         fields = ['ouvrage', 'etat', 'reserve']  # Exclude 'quantite' from fields
    
#     def __init__(self, *args, **kwargs):
#         super(ExemplaireForm, self).__init__(*args, **kwargs)
#         self.fields['ouvrage'].widget.attrs.update({'class': 'form-control'})
#         self.fields['etat'].widget.attrs.update({'class': 'form-control'}) 
#         self.fields['reserve'].widget = forms.CheckboxInput()
        
#         # Hide 'quantite' field in update case
#         if self.instance.pk:
#             self.fields['quantite'].widget = forms.HiddenInput()
        
            
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_reservation', 'date_retour_prevue']  # Include 'return_date' field in the form fields
        
    def __init__(self, *args, ouvrage_instance=None, **kwargs):  
        super().__init__(*args, **kwargs)
        self.fields['date_reservation'].widget = forms.DateInput(attrs={'type': 'date', 'id': 'id_date_reservation','class': 'form-control'})
        self.fields['date_retour_prevue'].widget = forms.DateInput(attrs={'type': 'date', 'id': 'id_date_retour_prevue','class': 'form-control'})
        
        # if ouvrage_instance: 
        #     self.fields['ouvrage'].queryset = Ouvrage.objects.filter(pk=ouvrage_instance.pk)
        #     self.fields['ouvrage'].initial = ouvrage_instance.titre
        #     self.fields['ouvrage'].widget = forms.TextInput(attrs={'disabled': True, 'class': 'form-control'})

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

# class EmpruntForm(forms.ModelForm):
#     CNE = forms.CharField(max_length=20, required=False, label='CNE', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNE'}))
#     nom = forms.CharField(max_length=100, required=False, label='Nom', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}))
#     prenom = forms.CharField(max_length=100, required=False, label='Prénom', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}))

#     class Meta:
#         model = Emprunt
#         fields = ['CNE', 'nom', 'prenom', 'exemplaire', 'date_retour', 'automatique', 'confirmer', 'rendu']
#         widgets = {
#             'exemplaire': forms.Select(attrs={'class': 'form-control'}),
#             'date_retour': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'automatique': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'confirmer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'rendu': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # Filter to show only available exemplaires
#         exemplaire_qs = Exemplaire.objects.filter(etat='DISPONIBLE')
        
#         if self.instance and self.instance.pk:
#             emprunteur = getattr(self.instance, 'emprunteur', None)
#             if emprunteur:
#                 self.fields['CNE'].initial = emprunteur.CNE
#                 self.fields['nom'].initial = emprunteur.nom
#                 self.fields['prenom'].initial = emprunteur.prenom
            
#             # Include the current exemplaire in the queryset if the instance exists and has an exemplaire
#             exemplaire_actuel = getattr(self.instance, 'exemplaire', None)
#             if exemplaire_actuel:
#                 exemplaire_qs = Exemplaire.objects.filter(pk=exemplaire_actuel.pk) | exemplaire_qs

#         self.fields['exemplaire'].queryset = exemplaire_qs

#     def clean(self):
#         cleaned_data = super().clean()
#         CNE = cleaned_data.get('CNE')
#         nom = cleaned_data.get('nom')
#         prenom = cleaned_data.get('prenom')
#         exemplaire = cleaned_data.get('exemplaire')

#         # Search for the corresponding user by CNE
#         if CNE:
#             emprunteurs = Profile.objects.filter(CNE=CNE)
#             if emprunteurs.exists():
#                 emprunteur = emprunteurs.first()
#             else:
#                 self.add_error('CNE', ValidationError("Aucun utilisateur trouvé avec ce CNE."))
#         # Search for the corresponding user by name and surname
#         elif nom and prenom:
#             emprunteurs = Profile.objects.filter(nom=nom, prenom=prenom)
#             if emprunteurs.exists():
#                 emprunteur = emprunteurs.first()
#             else:
#                 self.add_error('nom', ValidationError("Aucun utilisateur trouvé avec ce nom et prénom."))
#                 self.add_error('prenom', ValidationError("Aucun utilisateur trouvé avec ce nom et prénom."))
#         else:
#             raise ValidationError("Veuillez fournir le CNE ou le nom et prénom.")

#         # Add verification here
#         if Emprunt.objects.filter(emprunteur=emprunteur, rendu=False).exclude(pk=self.instance.pk).exists():
#             raise ValidationError("Cet utilisateur a déjà un emprunt non rendu.")

#         cleaned_data['emprunteur'] = emprunteur

#         # Verify if the exemplaire is available
#         if exemplaire is not None:
#             if exemplaire.etat != 'DISPONIBLE' and exemplaire != getattr(self.instance, 'exemplaire', None):
#                 self.add_error('exemplaire', ValidationError("Cet exemplaire n'est pas disponible"))

#         # Verify if the return date is defined
#         date_retour = cleaned_data.get('date_retour')
#         if not date_retour:
#             cleaned_data['date_retour'] = datetime.now().date() + timedelta(days=15)

#         return cleaned_data
from django.core.exceptions import ValidationError

class EmpruntForm(forms.ModelForm):
    CNE = forms.ModelChoiceField(
        queryset=Profile.objects.exclude(CNE__isnull=True).exclude(CNE=''),  # Filtrer les profils sans CNE
        required=False,
        label='CNE',
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionner un CNE'}),
        to_field_name='CNE'  # Assurez-vous que la sélection est basée sur le CNE
    )
    nom = forms.CharField(max_length=100, required=False, label='Nom', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}))
    prenom = forms.CharField(max_length=100, required=False, label='Prénom', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}))

    class Meta:
        model = Emprunt
        fields = ['CNE', 'nom', 'prenom', 'exemplaire', 'date_retour', 'automatique', 'confirmer', 'rendu']
        widgets = {
            'exemplaire': forms.Select(attrs={'class': 'form-control'}),
            'date_retour': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'automatique': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'confirmer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rendu': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customizing the CNE field choices to display CNE instead of the default string representation
        self.fields['CNE'].queryset = Profile.objects.exclude(CNE__isnull=True).exclude(CNE='')  # Exclude profiles without CNE
        self.fields['CNE'].label_from_instance = lambda obj: f'{obj.CNE}'  # Display CNE

        # Filter to show only available exemplaires
        exemplaire_qs = Exemplaire.objects.filter(etat='DISPONIBLE')
        
        if self.instance and self.instance.pk:
            emprunteur = getattr(self.instance, 'emprunteur', None)
            if emprunteur:
                self.fields['CNE'].initial = emprunteur.CNE
                self.fields['nom'].initial = emprunteur.nom
                self.fields['prenom'].initial = emprunteur.prenom
            
            # Include the current exemplaire in the queryset if the instance exists and has an exemplaire
            exemplaire_actuel = getattr(self.instance, 'exemplaire', None)
            if exemplaire_actuel:
                exemplaire_qs = Exemplaire.objects.filter(pk=exemplaire_actuel.pk) | exemplaire_qs

        self.fields['exemplaire'].queryset = exemplaire_qs

    def clean(self):
        cleaned_data = super().clean()
        CNE = cleaned_data.get('CNE')
        nom = cleaned_data.get('nom')
        prenom = cleaned_data.get('prenom')
        exemplaire = cleaned_data.get('exemplaire')

        # Check if the CNE is provided
        if CNE:
            emprunteur = CNE  # Since CNE is now a ModelChoiceField, it will return a Profile instance selected by CNE
        # Search for the corresponding user by name and surname if CNE is not provided
        elif nom and prenom:
            emprunteurs = Profile.objects.filter(nom=nom, prenom=prenom)
            if emprunteurs.exists():
                emprunteur = emprunteurs.first()
            else:
                self.add_error('nom', ValidationError("Aucun utilisateur trouvé avec ce nom et prénom."))
                self.add_error('prenom', ValidationError("Aucun utilisateur trouvé avec ce nom et prénom."))
        else:
            raise ValidationError("Veuillez fournir le CNE ou le nom et prénom.")

        # Add verification here
        if Emprunt.objects.filter(emprunteur=emprunteur, rendu=False).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Cet utilisateur a déjà un emprunt non rendu.")

        cleaned_data['emprunteur'] = emprunteur

        # Verify if the exemplaire is available
        if exemplaire is not None:
            if exemplaire.etat != 'DISPONIBLE' and exemplaire != getattr(self.instance, 'exemplaire', None):
                self.add_error('exemplaire', ValidationError("Cet exemplaire n'est pas disponible"))

        # Verify if the return date is defined
        date_retour = cleaned_data.get('date_retour')
        if not date_retour:
            cleaned_data['date_retour'] = datetime.now().date() + timedelta(days=15)
        return cleaned_data
