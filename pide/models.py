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


class Examen(models.Model):
    nom = models.CharField(max_length=100)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='examens')
    date = models.DateField()
    duree = models.IntegerField()  # ou IntegerField() si tu préfères spécifier en minutes
    nombre_questions = models.PositiveIntegerField(default=0)  # Champ pour le nombre de questions

    def __str__(self):
        return self.nom


class Question(models.Model):
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='questions')
    intitule = models.CharField(max_length=255)

    def __str__(self):
        return self.intitule


class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses')
    intitule = models.CharField(max_length=255)
    est_correcte = models.BooleanField(default=False)  # pour indiquer si c'est la bonne réponse

    def __str__(self):
        return self.intitule
