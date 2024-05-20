from django.urls import path
from . import views

app_name = 'ouvrages'

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('browse', views.browse, name="browse"),
    path('categories/', views.categories, name="categories"),
    path('ouvrages', views.ouvrages, name="ouvrages"),
    path('ouvrage/<str:pk>', views.ouvrage, name="ouvrage"),
    #other options: <int:pk>, <id:pk>, <slug:pk>
    path('create-ouvrage/', views.createOuvrage, name="create-ouvrage"),
    path('update-ouvrage/<str:pk>', views.updateOuvrage, name="update-ouvrage"),
    path('delete-ouvrage/<str:pk>', views.deleteOuvrage, name="delete-ouvrage"),
    path('topics-detail/', views.topicsDetail, name="topics-detail"),
    path('topics-listing/', views.topicsListing, name="topics-listing"),
    # path('contact/', views.contact, name="contact"),
    path('exemplaires/', views.exemplaires, name="exemplaires"),
    path('exemplaire/<str:pk>', views.exemplaire, name="exemplaire"),
    #other options: <int:pk>, <id:pk>, <slug:pk>
    path('create-exemplaire/', views.createExemplaire, name="create-exemplaire"),
    path('update-exemplaire/<str:pk>', views.updateExemplaire, name="update-exemplaire"),
    path('delete-exemplaire/<str:pk>', views.deleteExemplaire, name="delete-exemplaire"),
    path('search-exemplaires/', views.search_exemplaires, name='search_exemplaires'),
    path('modifier_exemplaire/<str:pk>/', views.modifier_exemplaire, name='modifier_exemplaire'),
    path('emprunt/', views.liste_emprunts, name="emprunt"),
    path('nouvel-emprunt/',views.nouvel_emprunt, name='nouvel_emprunt'),
     path('supprimer_emprunt/<uuid:emprunt_id>/', views.supprimer_emprunt, name='supprimer_emprunt'),
    #reservations
    path('list_reservations/', views.list_reservations, name='list_reservations'),
    path('reservation_detail/<str:pk>', views.reservation_detail, name="reservation_detail"),
    path('myreservations/', views.user_reservations, name="user-reservations"),
    path('make-reservation/<str:pk>', views.makeReservation, name="make-reservation"),
    path('edit-reservation/<str:pk>', views.editReservation, name="edit-reservation"),
    path('cancel-reservation/<str:pk>', views.cancelReservation, name="cancel-reservation"),
]