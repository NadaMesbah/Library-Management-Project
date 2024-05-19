from django.forms import ModelForm
from .models import Ouvrage, Exemplaire, Reservation
from django.db import transaction
from django import forms
from django.forms.widgets import DateInput
from datetime import datetime, timedelta

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
            logger.info(f"Potential ID {potential_id} already exists. Generating a new one.")
            potential_id = f"FSM{get_random_string(length=4)}"
        logger.info(f"Generated unique ID: {potential_id}")
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
        self.fields['date_reservation'].widget = DateInput(attrs={'type': 'date', 'id': 'id_date_reservation','class': 'form-control'})
        self.fields['date_retour_prevue'].widget = DateInput(attrs={'type': 'date', 'id': 'id_date_retour_prevue','class': 'form-control'})
        
        # if ouvrage_instance: 
        #     self.fields['ouvrage'].queryset = Ouvrage.objects.filter(pk=ouvrage_instance.pk)
        #     self.fields['ouvrage'].initial = ouvrage_instance.titre
        #     self.fields['ouvrage'].widget = forms.TextInput(attrs={'disabled': True, 'class': 'form-control'})

