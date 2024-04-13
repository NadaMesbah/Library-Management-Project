from django.forms import ModelForm
from .models import Ouvrage, Exemplaire
from django import forms
class OuvrageForm(ModelForm):
    class Meta:
        model = Ouvrage
        fields = ['titre','featured_image', 'auteurs', 'description', 'categories', 'exemplaires_total']
        #fields = '__all__'

class ExemplaireForm(ModelForm):
    quantite = forms.IntegerField(label='Quantité')
    class Meta:
        model = Exemplaire
        fields = ['ouvrage', 'etat', 'emprunte', 'reserve']