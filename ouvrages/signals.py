from django.db.models.signals import post_save, post_delete

from django.db.models.signals import pre_delete

from django.utils.crypto import get_random_string


from django.dispatch import receiver
from .models import *
import logging

logger = logging.getLogger(__name__)

def generate_unique_id():
    # Generate a unique id
    potential_id = f"FSM{get_random_string(length=4)}"
    while Exemplaire.objects.filter(id=potential_id).exists():
        logger.info(f"Potential ID {potential_id} already exists. Generating a new one.")
        potential_id = f"FSM{get_random_string(length=4)}"
    logger.info(f"Generated unique ID: {potential_id}")
    return potential_id

@receiver(post_save, sender=Ouvrage)
def create_exemplaire_on_ouvrage_create(sender, instance, created, **kwargs):
    if created:
        exemplaires_count = Exemplaire.objects.filter(ouvrage=instance).count()
        logger.info(f"Creating exemplaire for ouvrage {instance}...")

        barcode = generate_unique_id()  # Generate the unique ID first

        if exemplaires_count == 0:
            exemplaire = Exemplaire.objects.create(ouvrage=instance, etat='HORS_PRET', id=barcode)
        else:
            exemplaire = Exemplaire.objects.create(ouvrage=instance, etat='DISPONIBLE', id=barcode)

        logger.info(f"Exemplaire created with ID {barcode}")
        
@receiver(post_save, sender=Exemplaire)
def update_exemplaires_total_on_save(sender, instance, created, **kwargs):
    if created:
        instance.ouvrage.update_exemplaires_total()

@receiver(post_delete, sender=Exemplaire)
def update_exemplaires_total_on_delete(sender, instance, **kwargs):
    instance.ouvrage.update_exemplaires_total()
        
# @receiver(post_save, sender=Exemplaire)
# def update_ouvrage_on_exemplaire_save(sender, instance, created, **kwargs):
#     if created:
#         instance.ouvrage.exemplaires_total += 1
#         instance.ouvrage.save()

# @receiver(post_delete, sender=Exemplaire)
# def update_ouvrage_on_exemplaire_delete(sender, instance, **kwargs):
#     instance.ouvrage.exemplaires_total -= 1
#     instance.ouvrage.save()


# @receiver(post_save, sender=Ouvrage)
# def create_exemplaire_on_ouvrage_create(sender, instance, created, **kwargs):
#     if created:
#         exemplaires_count = Exemplaire.objects.filter(ouvrage=instance).count()
#         if exemplaires_count == 0:
#             exemplaire = Exemplaire.objects.create(ouvrage=instance, etat='HORS_PRET')
#         else:
#             exemplaire = Exemplaire.objects.create(ouvrage=instance, etat='DISPONIBLE')

#         barcode = generate_unique_id()
#         exemplaire.id = barcode
#         exemplaire.save()

@receiver(pre_delete, sender=Reservation)
def pre_delete_reservation(sender, instance, **kwargs):
    exemplaire = instance.selected_copy
    exemplaire.etat = 'DISPONIBLE'
    exemplaire.reserve = False
    exemplaire.save()
