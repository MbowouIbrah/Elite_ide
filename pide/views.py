from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import InscriptionForm
from django.contrib import messages

# Fonction de test pour vérifier si l'utilisateur est promoteur ou formateur
def est_promoteur_ou_formateur(user):
    return user.is_authenticated and (
        user.groups.filter(name='promoteur').exists() or
        user.groups.filter(name='formateur').exists()
    )

def index(request):
    # Si l'utilisateur est connecté et a le rôle promoteur ou formateur, rediriger vers le dashboard
    if request.user.is_authenticated:
        if est_promoteur_ou_formateur(request.user):
            return redirect('dashboard')
    # Sinon, afficher la page index
    return render(request, "index.html")

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = InscriptionForm()

    return render(request, "inscription.html", {'form': form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Si l'utilisateur est promoteur ou formateur, rediriger vers le dashboard
            if est_promoteur_ou_formateur(user):
                return redirect('dashboard')
            else:
                return redirect('index')  # Rediriger vers index si l'utilisateur est candidat ou autre
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'connexion.html')

@login_required(login_url="/connexion/")
@user_passes_test(est_promoteur_ou_formateur, login_url="/index/")
def dashboard(request):
    # Préparer le contexte en fonction du rôle
    if request.user.groups.filter(name='formateur').exists():
        context = {'role': 1}
    elif request.user.groups.filter(name='promoteur').exists():
        context = {'role': 2}
    else:
        return redirect('index')  # Rediriger si le rôle n'est ni formateur ni promoteur

    return render(request, 'dashboard.html', context)

def deconnexion(request):
    logout(request)  # Déconnecter l'utilisateur
    return redirect('index')  # Redirection vers l'index
