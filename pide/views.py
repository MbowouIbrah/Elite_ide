from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import InscriptionForm, FormateurForm, FormationForm, PromoteurForm
from django.contrib import messages

# Vérifie si l'utilisateur est admin, promoteur ou formateur
def isAdministration(user):
    return user.role in ['admin', 'promoteur', 'formateur']

# Vérifie si l'utilisateur est admin
def isAdmin(user):
    return user.role == 'admin'

# Vérifie si l'utilisateur est promoteur
def isPro(user):
    return user.role == 'promoteur'

# Vue pour la page d'accueil
def index(request):
    if request.user.is_authenticated and isAdministration(request.user):
        return redirect('dashboard')  # Redirige vers le dashboard si l'utilisateur est connecté et autorisé
    return render(request, "index.html")

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

# Vue pour le tableau de bord (Dashboard)
@login_required(login_url="/connexion/")
@user_passes_test(isAdministration, login_url="/index/")
def dashboard(request):
    promoteur_form = PromoteurForm()
    formateur_form = FormateurForm()
    formation_form = FormationForm()
    if request.method == 'POST':
        if isAdmin(request.user):
            promoteur_form = PromoteurForm(request.POST)
            if promoteur_form.is_valid():
                promoteur_form.save()
                return redirect('dashboard')

        elif isPro(request.user):
            print('promoteur')
            if 'formateur' in request.POST:
                formateur_form = FormateurForm(request.POST)
                print('formateur : ' + str(formateur_form.is_valid()))
                if formateur_form.is_valid():
                    formateur_form.save()
                    return redirect('dashboard')
            elif 'formation' in request.POST:
                formation_form = FormationForm(request.POST)
                print('formation : ' + str(formation_form.is_valid()))
                if formation_form.is_valid():
                    formation_form.save()
                    return redirect('dashboard')
        
    else:
        promoteur_form = PromoteurForm()
        formateur_form = FormateurForm()
        formation_form = FormationForm()

    # Préparation du contexte en fonction du rôle
    context = {'promoteur_form': promoteur_form, 'formateur_form': formateur_form, 'formation_form': formation_form, 'role': get_user_role_context(request.user)}

    return render(request, 'dashboard.html', context)

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
