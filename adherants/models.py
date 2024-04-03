from django.db import models
from django.contrib.auth.models import AbstractUser

class Person(AbstractUser):
    # Common fields for all persons
    cni = models.CharField(max_lengh=8, primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    class Meta:
        abstract = True

class Adherant(Person):
    academic_email = models.EmailField(unique=True)

class Student(Adherant):
    cne = models.CharField(max_length=20, primary_key=True)
    filiere = models.CharField(max_length=50)
    semester = models.CharField(max_length=20)

class Professor(Adherant):
    pass  # no additional fields for now hihi
