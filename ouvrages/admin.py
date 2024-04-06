from django.contrib import admin
from .models import Ouvrage, Categorie, Auteur, Review, Rayon, Exemplaire, Emprunt, Reservation
# Register your models here.
admin.site.register(Ouvrage)
admin.site.register(Categorie)
admin.site.register(Auteur)
admin.site.register(Review)
admin.site.register(Rayon)
admin.site.register(Exemplaire)
admin.site.register(Emprunt)
admin.site.register(Reservation)