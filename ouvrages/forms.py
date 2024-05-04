from django.forms import ModelForm
from .models import Ouvrage, Exemplaire, Reservation
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
    quantite = forms.IntegerField(label='Quantité')
    exemplaire = forms.ModelChoiceField(queryset=Exemplaire.objects.filter(reserve=False, etat='DISPONIBLE'), label='Exemplaire')
    class Meta:
        model = Exemplaire
        fields = ['exemplaire', 'ouvrage', 'etat', 'reserve']

    def __init__(self, *args, **kwargs):
        super(ExemplaireForm, self).__init__(*args, **kwargs)
        self.fields['Exemplaire'] = forms.ModelChoiceField(queryset=Exemplaire.objects.filter(reserve=False, etat='DISPONIBLE'), label='Exemplaire')
        self.fields['Exemplaire'].widget.attrs.update({'class': 'form-control'})
        self.fields['ouvrage'].widget.attrs.update({'class': 'form-control'})
        self.fields['etat'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['reserve'].widget.attrs.update({'class': 'form-control'})  
        
            
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

