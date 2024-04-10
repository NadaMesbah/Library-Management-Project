from django.urls import path
from . import views

app_name = 'ouvrages'

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('browse', views.browse, name="browse"),
    path('ouvrages', views.ouvrages, name="ouvrages"),
    path('ouvrage/<str:pk>', views.ouvrage, name="ouvrage"),
    #other options: <int:pk>, <id:pk>, <slug:pk>
    path('create-ouvrage/', views.createOuvrage, name="create-ouvrage"),
    path('update-ouvrage/<str:pk>', views.updateOuvrage, name="update-ouvrage"),
    path('delete-ouvrage/<str:pk>', views.deleteOuvrage, name="delete-ouvrage"),
    path('topics-detail/', views.topicsDetail, name="topics-detail"),
    path('topics-listing/', views.topicsListing, name="topics-listing"),
    path('contact/', views.contact, name="contact"),
]