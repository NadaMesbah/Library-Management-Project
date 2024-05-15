from django.db.models.signals import post_save, post_delete

from django.db.models.signals import pre_delete

from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Exemplaire)
def update_ouvrage_on_exemplaire_save(sender, instance, created, **kwargs):
    if created:
        instance.ouvrage.exemplaires_total += 1
        instance.ouvrage.save()

@receiver(post_delete, sender=Exemplaire)
def update_ouvrage_on_exemplaire_delete(sender, instance, **kwargs):
    instance.ouvrage.exemplaires_total -= 1
    instance.ouvrage.save()

@receiver(post_save, sender=Ouvrage)
def create_exemplaire_on_ouvrage_create(sender, instance, created, **kwargs):
    if created:
        exemplaires_count = Exemplaire.objects.filter(ouvrage=instance).count()
        if exemplaires_count == 0:
            exemplaire = Exemplaire.objects.create(ouvrage=instance, etat='HORS_PRET')
        else:
            exemplaire = Exemplaire.objects.create(ouvrage=instance, etat='DISPONIBLE')

        barcode = exemplaire.generate_unique_id()
        exemplaire.id = barcode
        exemplaire.save()

@receiver(pre_delete, sender=Reservation)
def pre_delete_reservation(sender, instance, **kwargs):
    exemplaire = instance.selected_copy
    exemplaire.etat = 'DISPONIBLE'
    exemplaire.reserve = False
    exemplaire.save()
