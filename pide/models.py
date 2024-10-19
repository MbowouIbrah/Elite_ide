from django.db import models

# Create your models here.
class Utilisateurs(models.Model):
    nom = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    mdp = models.CharField(max_length=255, blank=True)