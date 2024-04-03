from django.db import models
from adherants.models import Person
from books.models import Emprunt
from books.models import Reservation

class Bibliothecaire(Person):
    # fields specific to Bibliothecaire
    id_B = models.CharField(max_length=20,primary_key=True, unique=True)

    def get_active_emprunts(self):
        # emprunts actifs
        return Emprunt.objects.filter(bibliothecaire=self, rendu=False)

    def get_emprunts_history(self):
        # historique des emprunts
        return Emprunt.objects.filter(bibliothecaire=self, rendu=True)

    def update_etat_exemplaire(self, exemplaire, new_etat):
        exemplaire.etat = new_etat
        exemplaire.save()
    
    def get_pending_reservations(self):
        #récupérer les réservations en attente gérées par ce bibliothécaire.
        return Reservation.objects.filter(bibliothecaire=self, acceptee=False)

    def accept_reservation(self, reservation):
        #accepter une réservation.
        reservation.acceptee = True
        reservation.save()

    def reject_reservation(self, reservation):
        #rejeter une réservation.
        reservation.delete()
