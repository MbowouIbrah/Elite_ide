# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    ROLES = [
        ('admin', 'Administrateur'),
        ('promoteur', 'Promoteur'),
        ('formateur', 'Formateur'),
        ('candidat', 'Candidat'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='candidat')
    is_active = models.BooleanField(default=True)
    formations = models.ManyToManyField('Formation', blank=True, related_name='formateurs')

    def __str__(self):
        return self.username


class Formation(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.titre
