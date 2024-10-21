from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur, Formation, Examen, Question, Reponse

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']



# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur, Formation

class FormateurForm(UserCreationForm):
    email = forms.EmailField(required=True)
    formations = forms.ModelMultipleChoiceField(
        queryset=Formation.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'formations']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'formateur'  # Fixer le rôle à formateur
        if commit:
            user.save()
            self.save_m2m()  # Enregistrer la relation ManyToMany
        return user




class PromoteurForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'promoteur'  # Fixer le rôle à promoteur
        if commit:
            user.save()
        return user



class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['titre', 'description', 'prix']  # Inclure le prix






class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['nom', 'formation', 'date', 'duree', 'nombre_questions']  # Inclure le champ ici


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['intitule']  # Le champ pour l'intitulé de la question

class ReponseForm(forms.ModelForm):
    class Meta:
        model = Reponse
        fields = ['intitule', 'est_correcte']  # Les champs pour la réponse
