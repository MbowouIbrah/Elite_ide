import os
import django

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projets.settings")  # Remplace ton_projet par le nom de ton projet
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    # Utiliser le modèle Utilisateur
    Utilisateur = get_user_model()

    # Détails de l'administrateur
    username = 'admin'
    email = 'admin@gmail.com'
    password = 'admin123'  # Changez ceci pour un mot de passe plus sécurisé
    nom = 'admin'
    prenom = 'test'
    role = 'admin'  # Assurez-vous que ce rôle est défini dans votre modèle

    # Créer l'utilisateur
    try:
        admin_user = Utilisateur.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=prenom,
            last_name=nom,
            role=role  # Assurez-vous d'assigner le rôle admin
        )
        print(f"Administrateur créé : {admin_user.username}")
    except Exception as e:
        print(f"Erreur lors de la création de l'administrateur : {e}")

if __name__ == '__main__':
    create_admin()
