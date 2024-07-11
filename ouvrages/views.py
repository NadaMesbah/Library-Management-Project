from django.shortcuts import render, redirect, get_object_or_404
from adherants.models import Profile
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Ouvrage, Categorie, Exemplaire, Reservation, Review, Profile, Emprunt
from django.db import transaction
from .forms import OuvrageForm, ExemplaireForm, ReservationForm, ReviewForm, EmpruntForm
from .utils import searchOuvrages, searchExemplaires, paginateOuvrages, paginateExemplaires, paginateReviews

from django.contrib.auth.decorators import user_passes_test


def index(request):
    ouvrages, search_query = searchOuvrages(request)
    #categories = ouvrage.categories.all() ==> ouvrage is an instance of Ouvrage
    #ouvrages = Ouvrage.objects.all()
    categories = Categorie.objects.all()
    ouvrage_count = ouvrages.count()
    best_ouvrage = Ouvrage.objects.exclude(vote_total=0).order_by('-vote_ratio').first()
    newest_ouvrage = Ouvrage.objects.order_by('-date_achat').first()
    recommended_ouvrages = Ouvrage.objects.filter(recommended=True)
    context = {'ouvrages': ouvrages, 'categories': categories,
               'ouvrage_count': ouvrage_count, 'best_ouvrage' : best_ouvrage, 
               'newest_ouvrage': newest_ouvrage , 'recommanded_ouvrages' : recommended_ouvrages, 'search_query': search_query}
    return render(request, 'ouvrages/index.html', context)

def browse(request):
    ouvrages, search_query = searchOuvrages(request)
    ouvrage_count = ouvrages.count()  # Count before pagination
    custom_range, paginated_ouvrages = paginateOuvrages(request, ouvrages, 3)
    categories = Categorie.objects.all()

    context = {
        'ouvrages': paginated_ouvrages,
        'categories': categories,
        'ouvrage_count': ouvrage_count,
        'search_query': search_query,
        'custom_range': custom_range,
        # 'exemplaires': exemplaires  # Comment this out or define exemplaires if needed
    }
    return render(request, 'ouvrages/browse-ouvrages.html', context)

def categories(request):
    keyword = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Categorie.objects.filter(
        Q(name__icontains=keyword)
    )
    categorie_count = categories.count()
    context = {'categories': categories}
    return render(request, 'ouvrages/categories.html', context)

def topicsDetail(request):
    return render(request, 'ouvrages/topics-detail.html')

def topicsListing(request):
    return render(request, 'ouvrages/topics-listing.html')

# def contact(request):
#     return render(request, 'adherants/contact.html')

def home(request):
    keyword = request.GET.get('keyword') if request.GET.get('keyword') != None else ''
    ouvrages = Ouvrage.objects.filter(
        Q(categories__name__icontains=keyword) |
        Q(titre__icontains=keyword) |
        Q(description__icontains=keyword)
    )          
    #categories = ouvrage.categories.all() ==> ouvrage is an instance of Ouvrage
    #ouvrages = Ouvrage.objects.all()
    categories = Categorie.objects.all()
    ouvrage_count = ouvrages.count()
    context = {'ouvrages': ouvrages, 'categories': categories,
               'ouvrage_count': ouvrage_count}
    return render(request, 'ouvrages/home.html', context)

def est_administrateur(user):
    return user.is_authenticated and user.is_staff

## CRUD FOR OUVRAGES   
def ouvrages(request):
    ouvrages = Ouvrage.objects.all().distinct()
    context = {'ouvrages': ouvrages}
    return render(request, 'ouvrages/ouvrages.html', context)

#whatever we name the parameter here <str:pk> we should name it here :
def ouvrage(request, pk):
    ouvrageObj = Ouvrage.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ouvrage = ouvrageObj
            review.owner = request.user.profile
            review.save()

            ouvrageObj.getVoteCount

            messages.success(request, 'Your review was successfully submitted!')
            return redirect('ouvrages:ouvrage', pk=ouvrageObj.id)

    reviews = ouvrageObj.review_set.all()
    custom_range, reviews = paginateReviews(request, reviews, 3)

    context = {
        'reviews': reviews,
        'custom_range': custom_range,
        'ouvrage': ouvrageObj,
        'form': form
    }
    return render(request, 'ouvrages/single-ouvrage.html', context)

@user_passes_test(est_administrateur)
def createOuvrage(request):
    page = 'add'
    form = OuvrageForm()
    if request.method == 'POST':
        form = OuvrageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ouvrages:browse')
    context = {'form': form, 'page': page}
    return render(request, 'ouvrages/ouvrage_form.html', context)

def updateOuvrage(request, pk):
    page = 'edit'
    ouvrage = get_object_or_404(Ouvrage, id=pk)
    form = OuvrageForm(instance=ouvrage)
    if request.method == 'POST':
        form = OuvrageForm(request.POST, request.FILES ,instance=ouvrage)
        if form.is_valid():
            form.save()
            return redirect('ouvrages:browse')
    context = {'form': form, 'page': page}
    return render(request, 'ouvrages/ouvrage_form.html', context)

@user_passes_test(est_administrateur)
def deleteOuvrage(request, pk):
    ouvrage = get_object_or_404(Ouvrage, id=pk)
    if request.method == 'POST':
        # If the request is POST, delete the ouvrage
        ouvrage.delete()
        return redirect('ouvrages:browse')
    # If the request is not POST, render the confirmation page
    context = {'ouvrage': ouvrage}
    return render(request, 'ouvrages/delete_ouvrage.html', context)

## CRUD FOR EXEMPLAIRES
# def exemplaires(request):
#     exemplaires = Exemplaire.objects.all()
#     context = {'exemplaires': exemplaires}
#     return render(request, 'ouvrages/exemplaires.html', context)

def exemplaires(request):
    exemplaires, search_query = searchExemplaires(request)
    exemplaires_count = exemplaires.count() # Count before pagination
    custom_range, paginated_exemplaires = paginateExemplaires(request, exemplaires, 3)
    context = {
        'exemplaires': paginated_exemplaires,
        'exemplaires_count': exemplaires_count,
        'search_query': search_query,
        'custom_range': custom_range,
        # 'exemplaires': exemplaires  # Comment this out or define exemplaires if needed
    }
    return render(request, 'ouvrages/exemplaires.html', context)

def exemplaire(request, pk):
    exemplaireObj = Exemplaire.objects.get(id=pk)
    context = {'exemplaire': exemplaireObj}
    return render(request, 'ouvrages/single-exemplaire.html', context)



# def createExemplaire(request):
#     page = 'add'
#     form = ExemplaireForm()
#     if request.method == 'POST':
#         form = ExemplaireForm(request.POST)
#         if form.is_valid():
#             quantite = form.cleaned_data['quantite']
#             ouvrage_instance = form.cleaned_data['ouvrage']

#             exemplaires_data = [
#                 {'ouvrage': ouvrage_instance,
#                  'etat': form.cleaned_data['etat'],
#                  'reserve': form.cleaned_data['reserve'],
#                  'id': generate_unique_id()}
#                 for _ in range(quantite)
#             ]
            
#             Exemplaire.objects.bulk_create([Exemplaire(**data) for data in exemplaires_data])
#             return redirect('ouvrages:exemplaires')
#     context = {'form': form, 'page': page}
#     return render(request, 'ouvrages/exemplaire_form.html', context)

@user_passes_test(est_administrateur)
def createExemplaire(request):
    page = 'add'
    form = ExemplaireForm()
    if request.method == 'POST':
        form = ExemplaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ouvrages:exemplaires')  # Adjust this redirect to match your actual URL name
    context = {'form': form, 'page': page}
    return render(request, 'ouvrages/exemplaire_form.html', context)


# def generate_unique_id():
#     # Generate a unique id
#     while True:
#         potential_id = f"FSM{get_random_string(length=4)}"
#         if not Exemplaire.objects.filter(id=potential_id).exists():
#             return potential_id

@user_passes_test(est_administrateur)
def updateExemplaire(request, pk):
    page = 'edit'
    exemplaire = get_object_or_404(Exemplaire, id=pk)
    form = ExemplaireForm(instance=exemplaire)
    if request.method == 'POST':
        form = ExemplaireForm(request.POST ,instance=exemplaire)
        if form.is_valid():
            form.save()
            return redirect('ouvrages:exemplaires')
    context = {'form': form, 'page' : page}
    return render(request, 'ouvrages/exemplaire_form.html', context)

@user_passes_test(est_administrateur)
def deleteExemplaire(request, pk):
    exemplaire = get_object_or_404(Exemplaire, id=pk)
    if request.method == 'POST':
        # If the request is POST, delete the ouvrage
        exemplaire.delete()
        return redirect('ouvrages:exemplaires')
    # If the request is not POST, render the confirmation page
    context = {'exemplaire': exemplaire}
    return render(request, 'ouvrages/delete_exemplaire.html', context)

def makeReservation(request, pk):
    page = 'make'
    ouvrage = get_object_or_404(Ouvrage, id=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.ouvrage = ouvrage
            reservation.owner = request.user.profile
            reservation.save()
            messages.success(request, "Your reservation has been successfully created.")
            return redirect('ouvrages:user-reservations')
    else:
        # Use the form with ouvrage_instance only
        form = ReservationForm(ouvrage_instance=ouvrage)

    context = {'form': form, 'page' : page}
    return render(request, 'ouvrages/reservation_form.html', context)

def editReservation(request, pk):
    # Retrieve the existing reservation instance
    page = 'edit'
    reservation = get_object_or_404(Reservation, id=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)  # Pass instance to edit existing reservation
        if form.is_valid():
            form.save()
            messages.success(request, "Your reservation has been successfully updated.")
            return redirect('ouvrages:user-reservations')
    else:
        # Pass instance argument to the form for better handling of related fields
        form = ReservationForm(instance=reservation)
    
    context = {'form': form, 'page': page}
    return render(request, 'ouvrages/reservation_form.html', context)

def cancelReservation(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    if request.method == 'POST':
        # If the request is POST, delete the ouvrage
        if reservation.statut == 'acceptee':
            exemplaire = reservation.selected_copy
            exemplaire.etat = 'DISPONIBLE'
            exemplaire.reserve = False
            exemplaire.save()
        reservation.delete()
        return redirect('ouvrages:user-reservations')
    # If the request is not POST, render the confirmation page
    context = {'reservation': reservation}
    return render(request, 'ouvrages/cancel_reservation.html', context)

def user_reservations(request):
    reservations = Reservation.objects.filter(owner=request.user.profile)
    return render(request, 'ouvrages/myreservations.html', {'reservations': reservations})
# def reserver(request):
#     if request.method == 'POST':
#         owner = Profile.objects.get(email=request.user.email)

#         reservation_date_str = request.POST.get('datepicker')

#         reservation_date = datetime.strptime(reservation_date_str, '%m/%d/%Y')

#         day_name = reservation_date.strftime("%A")
        
#         print("Adherant: ", owner.email)
#         print("day_name: ", day_name)

#         Reservation.objects.create(
#              owner=owner,
#              date_reservation=reservation_date,
#         )
#         messages.success(
#             request, "Your reservation has been successfully created.")
#         return redirect('panel')
#     else:
#         return render(request, 'panel.html')

@user_passes_test(est_administrateur)
def list_reservations(request):
    # Supprimer les réservations expirées
    supprimer_reservations_expirees(request)
    # Récupérer toutes les réservations depuis la base de données
    reservations = Reservation.objects.all()
    # Passer les réservations au template
    return render(request, 'ouvrages/list_reservations.html', {'reservations': reservations})

@user_passes_test(est_administrateur)
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    
    # Vérifier si l'utilisateur a un emprunt non rendu
    has_unreturned_loan = Emprunt.objects.filter(emprunteur=reservation.owner, rendu=False).exists()

    if request.method == 'POST':
        # Annuler la réservation
        if 'cancel_reservation' in request.POST:
            selected_copy_id = request.POST.get('selected_copy')
            exemplaire = Exemplaire.objects.get(id=selected_copy_id)
            exemplaire.etat = 'DISPONIBLE'
            exemplaire.reserve = False
            exemplaire.save()  # Sauvegarder l'exemplaire après avoir mis à jour ses attributs
            reservation.delete()
            return redirect('ouvrages:list_reservations')
        
        # Accepter un exemplaire
        elif 'accept_copy' in request.POST and not has_unreturned_loan:
            selected_copy_id = request.POST.get('selected_copy')
            selected_copy = Exemplaire.objects.get(id=selected_copy_id)
            selected_copy.reserve = True
            selected_copy.etat = 'HORS_PRET'
            selected_copy.save()
            reservation.ouvrage = selected_copy.ouvrage  # Utiliser l'ouvrage lié à l'exemplaire
            reservation.selected_copy = selected_copy
            reservation.statut = 'acceptee'  # Mettre à jour le statut de la réservation
            reservation.save()

            # Créer un nouvel emprunt
            Emprunt.objects.create(
                emprunteur=reservation.owner,
                exemplaire=selected_copy,
                date_emprunt=reservation.date_reservation,
                date_retour=reservation.date_retour_prevue
            )
            return redirect('ouvrages:list_reservations')

    book_exemplaires = Exemplaire.objects.filter(ouvrage=reservation.ouvrage, reserve=False)
    return render(request, 'ouvrages/reservation_detail.html', {
        'reservation': reservation,
        'book_exemplaires': book_exemplaires,
        'has_unreturned_loan': has_unreturned_loan
    })


@user_passes_test(est_administrateur)
def supprimer_reservations_expirees(request):
    # Récupérer les réservations expirées (plus de 24 heures)
    reservations_expirees = Reservation.objects.filter(date_retour_prevue__lte=timezone.now())

    # Parcourir les réservations expirées
    for reservation in reservations_expirees:
        # Vérifier si la réservation a un exemplaire associé
        exemplaire = reservation.selected_copy
        if exemplaire:
            # Marquer l'exemplaire comme disponible
            exemplaire.etat = 'DISPONIBLE'
            exemplaire.reserve = False
            exemplaire.save()

            # Supprimer la réservation expirée
            reservation.delete()

@user_passes_test(est_administrateur)
def search_exemplaires(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword:
            exemplaires = Exemplaire.objects.filter(ouvrage__titre__icontains=keyword)
            return render(request, 'ouvrages/details_exemplaires.html', {'exemplaires': exemplaires, 'keyword': keyword})
        else:
            return render(request, 'ouvrages/details_exemplaires.html', {'exemplaires': None, 'keyword': None})
    else:
        return render(request, 'ouvrages/details_exemplaires.html', {'exemplaires': None, 'keyword': None})

@user_passes_test(est_administrateur)  
def modifier_exemplaire(request, pk):
    exemplaire = get_object_or_404(Exemplaire, id=pk)
    if request.method == 'POST':
        form = ExemplaireForm(request.POST, instance=exemplaire)
        if form.is_valid():
            form.save()
            return redirect('ouvrages:exemplaire', pk=pk)
    else:
        form = ExemplaireForm(instance=exemplaire)
    return render(request, 'ouvrages:modifier_exemplaire.html', {'form': form})

# def updateExemplaire(request, pk):
#     exemplaire = get_object_or_404(Exemplaire, id=pk)
#     form = ExemplaireForm(instance=exemplaire)
#     if request.method == 'POST':
#         form = ExemplaireForm(request.POST ,instance=exemplaire)
#         if form.is_valid():
#             form.save()
#             return redirect('ouvrages:exemplaires')
#     context = {'form': form}
#     return render(request, 'ouvrages/exemplaire_form.html', context)

# def liste_etudiants(request):
#     etudiants = Profile.objects.filter(user__is_staff=False)
#     return render(request, 'liste_etudiants.html', {'etudiants': etudiants})

@user_passes_test(est_administrateur)
def liste_emprunts(request):
    # Supprimer les emprunts automatiques non confirmés
    supprimer_emprunts_non_confirmes(request)

     # Supprimer les emprunts rendus
    emprunts_rendus = Emprunt.objects.filter(rendu=True)
    for emprunt_rendu in emprunts_rendus:
        # Marquer l'exemplaire comme disponible
        exemplaire = emprunt_rendu.exemplaire
        exemplaire.etat = 'DISPONIBLE'
        exemplaire.reserve = False
        exemplaire.save()

    # Supprimer les emprunts rendus
    emprunts_rendus.delete()

    # Récupérer tous les emprunts
    emprunts = Emprunt.objects.all()

    # Afficher la liste des emprunts dans un template
    return render(request, 'ouvrages/emprunt.html', {'emprunts': emprunts})


# @user_passes_test(est_administrateur)
# def nouvelEmprunt(request):
#     if request.method == 'POST':
#         form = EmpruntForm(request.POST)
#         if form.is_valid():
#             emprunt = form.save(commit=False)
#             emprunteur = form.cleaned_data['emprunteur']
#             emprunt.emprunteur = emprunteur
#             emprunt.automatique = False
#             emprunt.save()

#             # Marquer l'exemplaire comme emprunté
#             exemplaire = emprunt.exemplaire
#             exemplaire.etat = 'HORS_PRET'
#             exemplaire.save()

#             # Vérifier s'il existe une réservation acceptée pour cet exemplaire
#             reservation = Reservation.objects.filter(ouvrage=exemplaire.ouvrage, statut='acceptee').first()
#             if reservation:
#                 # Vérifier s'il n'existe pas déjà un emprunt automatique pour cet exemplaire
#                 existing_automatique = Emprunt.objects.filter(exemplaire=exemplaire, automatique=True).exists()
#                 if not existing_automatique:
#                     # Créer un nouvel emprunt avec les détails de la réservation
#                     Emprunt.objects.create(
#                         emprunteur=reservation.owner,
#                         exemplaire=exemplaire,
#                         date_emprunt=reservation.date_reservation,
#                         date_retour=reservation.date_retour_prevue,
#                         automatique=True,  # Marquer comme un emprunt automatique
#                         confirmer=False,   # L'emprunt n'est pas encore confirmé
#                     )

#             # Rediriger vers la liste des emprunts
#             return redirect('ouvrages:emprunt')
#     else:
#         form = EmpruntForm()
#     return render(request, 'ouvrages/nouvel_emprunt.html', {'form': form})
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Profile

def get_profile_info(request, cne):
    profile = get_object_or_404(Profile, CNE=cne)
    data = {
        'nom': profile.nom,
        'prenom': profile.prenom,
    }
    return JsonResponse(data)

@user_passes_test(est_administrateur)
def nouvelEmprunt(request):
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        if form.is_valid():
            emprunt = form.save(commit=False)
            emprunteur = form.cleaned_data['emprunteur']
            emprunt.emprunteur = emprunteur
            emprunt.automatique = False
            emprunt.save()

            # Marquer l'exemplaire comme emprunté
            exemplaire = emprunt.exemplaire
            exemplaire.etat = 'HORS_PRET'
            exemplaire.save()

            # Vérifier s'il existe une réservation acceptée pour cet exemplaire spécifique
            reservation = Reservation.objects.filter(ouvrage=exemplaire.ouvrage, selected_copy=exemplaire, statut='acceptee').first()
            if reservation:
                # Vérifier s'il n'existe pas déjà un emprunt automatique pour cet exemplaire
                existing_automatique = Emprunt.objects.filter(exemplaire=exemplaire, automatique=True).exists()
                if not existing_automatique:
                    # Créer un nouvel emprunt avec les détails de la réservation
                    Emprunt.objects.create(
                        emprunteur=reservation.owner,
                        exemplaire=exemplaire,
                        date_emprunt=reservation.date_reservation,
                        date_retour=reservation.date_retour_prevue,
                        automatique=True,  # Marquer comme un emprunt automatique
                        confirmer=False,   # L'emprunt n'est pas encore confirmé
                    )

            # Rediriger vers la liste des emprunts
            return redirect('ouvrages:emprunt')
    else:
        form = EmpruntForm()
    return render(request, 'ouvrages/nouvel_emprunt.html', {'form': form})

@user_passes_test(est_administrateur)
def modifier_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)

    if request.method == 'POST':
        form = EmpruntForm(request.POST, instance=emprunt)
        if form.is_valid():
            if form.cleaned_data.get('rendu'):
                emprunt.exemplaire.etat = 'DISPONIBLE'
                emprunt.exemplaire.reserve = False
                emprunt.exemplaire.save()
                emprunt.delete()
                messages.success(request, "L'emprunt a été marqué comme rendu et supprimé avec succès.")
                return redirect('ouvrages:emprunt')
            else:
                form.save()
                messages.success(request, "L'emprunt a été modifié avec succès.")
                return redirect('ouvrages:emprunt')
    else:
        form = EmpruntForm(instance=emprunt)

    return render(request, 'ouvrages/modifier_emprunt.html', {'form': form})

@user_passes_test(est_administrateur)
def deleteEmprunt(request, pk):
    emprunt = get_object_or_404(Emprunt, id=pk)
    if request.method == 'POST':
        # If the request is POST, delete the ouvrage
        emprunt.delete()
        return redirect('ouvrages:emprunt')
    # If the request is not POST, render the confirmation page
    context = {'emprunt': emprunt}
    return render(request, 'ouvrages/delete_emprunt.html', context)

@user_passes_test(est_administrateur)
def supprimer_emprunts_non_confirmes(request):
    # Récupérer tous les emprunts automatiques non confirmés
    emprunts_non_confirmes = Emprunt.objects.filter(
        automatique=True,
        confirmer=False,
        date_emprunt__lte=timezone.now() - timedelta(hours=24)
    )

   # Supprimer les emprunts non confirmés et mettre à jour l'état des exemplaires
    for emprunt in emprunts_non_confirmes:
        # Supprimer l'emprunt et vérifier s'il est supprimé avec succès
        if emprunt.delete()[0] == 1:
            # Mettre à jour l'état de l'exemplaire associé uniquement si l'emprunt est supprimé
            exemplaire = emprunt.exemplaire
            exemplaire.etat = 'DISPONIBLE'
            exemplaire.reserve = False  
            exemplaire.save()

@user_passes_test(est_administrateur)
def supprimer_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)
    exemplaire = emprunt.exemplaire

    # Supprimer l'emprunt
    emprunt.delete()

    # Marquer l'exemplaire comme disponible
    exemplaire.etat = 'DISPONIBLE'
    exemplaire.reserve = False
    exemplaire.save()

    return JsonResponse({'message': "L'emprunt a été supprimé avec succès."})
