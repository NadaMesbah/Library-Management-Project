from django.forms import ModelForm
from .models import Ouvrage

class OuvrageForm(ModelForm):
    class Meta:
        model = Ouvrage
        fields = ['titre', 'auteurs', 'description', 'categories', 'exemplaires_total']
        #fields = '__all__'