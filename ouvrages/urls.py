from django.urls import path
from . import views

urlpatterns = [
    path('', views.ouvrages, name="ouvrages"),
    path('ouvrage/<str:pk>', views.ouvrage, name="ouvrage"),
    #other options: <int:pk>, <id:pk>, <slug:pk>
    path('create-ouvrage/', views.createOuvrage, name="create-ouvrage"),
    path('update-ouvrage/<str:pk>', views.updateOuvrage, name="update-ouvrage"),
    path('delete-ouvrage/<str:pk>', views.deleteOuvrage, name="delete-ouvrage"),
]