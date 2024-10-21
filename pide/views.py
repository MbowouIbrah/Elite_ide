from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import InscriptionForm, FormateurForm, FormationForm, PromoteurForm, ExamenForm, QuestionForm, ReponseForm
from django.contrib import messages
from django.forms import modelformset_factory
from .models import Examen, Question, Reponse, Formation, Utilisateur


# Vérifie si l'utilisateur est admin, promoteur ou formateur
def isAdministration(user):
    return user.role in ['admin', 'promoteur', 'formateur']

# Vérifie si l'utilisateur est admin
def isAdmin(user):
    return user.role == 'admin'

# Vérifie si l'utilisateur est promoteur
def isPro(user):
    return user.role == 'promoteur'

# Vérifie si l'utilisateur est formateur
def isFor(user):
    return user.role == 'formateur'



# Vue pour la page d'accueil
def index(request):
    context = {
        'formations': Formation.objects.all(),
    }
    if request.user.is_authenticated and isAdministration(request.user):
        return redirect('dashboard')  # Redirige vers le dashboard si l'utilisateur est connecté et autorisé
    return render(request, "index.html", context)

# Vue pour l'inscription
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            return redirect('index')
    else:
        form = InscriptionForm()

    return render(request, "inscription.html", {'form': form})

@login_required(login_url="/connexion/")
@user_passes_test(isAdministration, login_url="/index/")
def dashboard(request):
    promoteur_form = PromoteurForm(request.POST or None)
    formateur_form = FormateurForm(request.POST or None)
    formation_form = FormationForm(request.POST or None)
    examen_form = ExamenForm(request.POST or None)

    candidats, formateurs, promoteurs, examens = [], [], [], []

    if request.method == 'POST':
        try:
            if isAdmin(request.user) and promoteur_form.is_valid():
                promoteur_form.save()
            elif isPro(request.user):
                if 'formateur' in request.POST and formateur_form.is_valid():
                    formateur_form.save()
                elif 'formation' in request.POST and formation_form.is_valid():
                    formation_form.save()
            elif isFor(request.user) and examen_form.is_valid():
                examen = examen_form.save(commit=False)
                examen.save()
            return redirect('dashboard')
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    if isFor(request.user) or isPro(request.user) or isAdmin(request.user):
        candidats = Utilisateur.objects.filter(role='candidat')
        examens = get_examens_utilisateur(request.user)
    if isPro(request.user) or isAdmin(request.user):
        formateurs = Utilisateur.objects.filter(role="formateur")
    if isAdmin(request.user):
        promoteurs = Utilisateur.objects.filter(role="promoteur")

    context = {
        'promoteur_form': promoteur_form,
        'formateur_form': formateur_form,
        'formation_form': formation_form,
        'examen_form': examen_form,
        'formations': Formation.objects.all(),
        'candidats': candidats,
        'formateurs': formateurs,
        'promoteurs': promoteurs,
        'examens': examens,
        'role': get_user_role_context(request.user)
    }

    return render(request, 'dashboard.html', context)



# Vue pour récupérer les examens liés aux formations d'un utilisateur
def get_examens_utilisateur(utilisateur):
    # Récupérer toutes les formations associées à cet utilisateur
    formations = utilisateur.formations.all()

    # Récupérer les examens liés à ces formations
    examens = Examen.objects.filter(formation__in=formations)

    return examens



# Fonction pour déterminer le rôle à afficher dans le tableau de bord
def get_user_role_context(user):
    if user.role == 'admin':
        return 3  # Rôle 3 : Administrateur
    elif user.role == 'promoteur':
        return 2  # Rôle 2 : Promoteur
    elif user.role == 'formateur':
        return 1  # Rôle 1 : Formateur
    else:
        return 0  # Rôle 0 : Autres utilisateurs non autorisés


def informations(request):

    return render(request, 'informations.html')


@login_required(login_url="/connexion/")
def formation(request):
    
    return render(request, 'formation.html')

# Vue pour la connexion
def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if isAdministration(user):
                return redirect('dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'connexion.html')

# Vue pour la déconnexion
def deconnexion(request):
    logout(request)
    return redirect('index')
