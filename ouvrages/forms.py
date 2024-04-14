from django.forms import ModelForm
from .models import Ouvrage, Exemplaire
from django import forms
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
        

class ExemplaireForm(ModelForm):
    quantite = forms.IntegerField(label='Quantité')
    class Meta:
        model = Exemplaire
        fields = ['ouvrage', 'etat', 'emprunte', 'reserve']
        
    def __init__(self, *args, **kwargs):
        super(ExemplaireForm, self).__init__(*args, **kwargs)
        self.fields['ouvrage'].widget.attrs.update({'class': 'form-control'})
        self.fields['etat'].widget.attrs.update({'class': 'form-control'})  