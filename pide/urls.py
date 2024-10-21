from django.urls import path
from . import views

urlpatterns =  [
    path('', views.index, name='index'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),  # Déconnexion
    path('informations/', views.informations, name='informations'),  # Déconnexion
    path('formation/', views.formation, name='formation'),  # Déconnexion
]