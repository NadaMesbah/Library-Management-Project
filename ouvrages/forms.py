from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from django.utils.crypto import get_random_string
from django.forms import ModelForm
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
            'categories': forms.CheckboxSelectMultiple(),
            'auteurs': forms.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        super(OuvrageForm, self).__init__(*args, **kwargs)
        self.fields['titre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ajouter un titre'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ajouter une description'})
        self.fields['exemplaires_total'].widget.attrs.update({'class': 'form-control'})
        self.fields['featured_image'].widget.attrs.update({'class': 'form-control'})
        

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


class EmpruntForm(forms.ModelForm):
    CNE = forms.CharField(max_length=20, required=False, label='CNE', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNE'}))
    nom = forms.CharField(max_length=100, required=False, label='Nom', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}))
    prenom = forms.CharField(max_length=100, required=False, label='Prénom', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}))

    class Meta:
        model = Emprunt
        fields = ['CNE', 'nom', 'prenom', 'exemplaire', 'date_retour']
        widgets = {
            'exemplaire': forms.Select(attrs={'class': 'form-control'}),
            'date_retour': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer pour ne montrer que les exemplaires disponibles
        self.fields['exemplaire'].queryset = Exemplaire.objects.filter(etat='DISPONIBLE')


    def clean(self):
        cleaned_data = super().clean()
        CNE = cleaned_data.get('CNE')
        nom = cleaned_data.get('nom')
        prenom = cleaned_data.get('prenom')
        exemplaire = cleaned_data.get('exemplaire')

        # Rechercher l'utilisateur correspondant
        if CNE:
            try:
                emprunteur = Profile.objects.get(CNE=CNE)
            except Profile.DoesNotExist:
                raise forms.ValidationError("Aucun utilisateur trouvé avec ce CNE.")
        elif nom and prenom:
            try:
                emprunteur = Profile.objects.get(nom=nom, prenom=prenom)
            except Profile.DoesNotExist:
                raise forms.ValidationError("Aucun utilisateur trouvé avec ce nom et prénom.")
        else:
            raise forms.ValidationError("Veuillez fournir le CNE ou le nom et prénom.")
        # Ajouter la vérification ici
        if Emprunt.objects.filter(emprunteur=emprunteur, rendu=False).exists():
            raise forms.ValidationError("Cet utilisateur a déjà un emprunt non rendu.")
        cleaned_data['emprunteur'] = emprunteur

        # Vérifiez si l'exemplaire est disponible
        if exemplaire is not None:
            if exemplaire.etat != 'DISPONIBLE':
                raise forms.ValidationError("Cet exemplaire n'est pas disponible")
            
        # Vérifiez si la date de retour est définie
        date_retour = cleaned_data.get('date_retour')
        if not date_retour:
            cleaned_data['date_retour'] = datetime.now().date() + timedelta(days=15)

        return cleaned_data
