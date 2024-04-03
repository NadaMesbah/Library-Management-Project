from django.db import models
import uuid

# Create your models here.

class Ouvrage(models.Model):
    code = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    titre = models.CharField(max_length=100)
    cover_image =models.ImageField(upload_to='img',blank=True,null=True)
    auteur=models.CharField(max_length=50)
    description =models.TextField()
    Categorie =models.ManyToManyField(Categorie,related_name='ouvrage')
    ouvrages_recommended =models.BooleanField(default=False)
    def _str_(self) :
        return self.titre
    
class Categorie (models.Model):
    name = models.CharField('Categories',max_length= 50)
    def _str_(self) :
        return self.name

class Rayon (models.Model):
    name = models.CharField('Rayon',max_length= 50)
    def _str_(self) :
        return self.name
    
class Exemplaire (models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    code_ouvrage = models.foreign_key(Ouvrage, db_index=True)

