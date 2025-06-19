from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.menu_view, name='menu_view'),
    #('form/', views.form_view, name='form'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
    path('save-beneficiaire/', views.save_beneficiaire, name='save_beneficiaire'),
    # Nouveaux chemins
    path('experimentation_form/', views.experimentation_form_view, name='experimentation_form'),
    path('create-experimentation/', views.create_experimentation, name='create_experimentation'),
    path('usager_pro_form/', views.usePro_Form_View, name='usePro_Form'),
    path("add-usager-pro/", views.add_usager_pro, name="add_usager_pro"),

    path('api/beneficiaire/<int:pk>/', views.BeneficiaireDetailView.as_view(), name='beneficiaire-detail'),
    path('api/beneficiaire/<int:pk>/update/', views.BeneficiaireUpdateView.as_view(), name='beneficiaire-update'),
    # New path for beneficiary details page
    path('beneficiaire/<int:pk>/', views.beneficiaire_detail_view, name='beneficiaire_detail'),
    path('experimentations/', views.liste_experimentations_view, name='liste_experimentations'),
    path('experimentations/<int:pk>/', views.experimentation_detail_view, name='experimentation_detail'),
    path('api/beneficiaire/<int:pk>/', views.BeneficiaireDetailView.as_view(), name='beneficiaire-detail'),
    path('api/beneficiaire/<int:pk>/update/', views.BeneficiaireUpdateView.as_view(), name='beneficiaire-update'),
    path('beneficiaire/<int:pk>/', views.beneficiaire_detail_view, name='beneficiaire_detail'),
    path('api/statuts-champs/', views.get_statuts_champs, name='get_statuts_champs'),
    # urls.py
    path('menu/', views.menu_view, name='menu'),
    path('ajouter-beneficiaire/', views.ajouter_beneficiaire_view, name='ajouter_beneficiaire'),
    path('api/statuts-champs/', views.api_statuts_champs, name='api_statuts_champs'),
    path('api/statuts-champs/', views.api_statuts_champs, name='api_statuts_champs'),
    path('form/', views.ajouter_beneficiaire_view, name='form_beneficiaire'),
    path('api/cibles/', views.api_cibles_experimentation, name='api_cibles_experimentation'),
    path('api/usagers/', views.api_usagers_par_statut, name='api_usagers_par_statut'),
    path('api/usagers/', views.api_usagers_par_statut, name='api_usagers_par_statut'),
    path('ajouter-usager-pro/', views.ajouter_usager_pro, name='ajouter_usager_pro'),
    path('api/usagers-pro/', views.api_usagers_pro, name='api_usagers_pro'),

    path('ajouter-usager/', views.ajouter_usager_ri2s, name='ajouter_usager_ri2s'),

    path('menu/', views.menu_view, name='menu'),
    path('api/options_dynamiques/', views.api_options_dynamiques, name='api_options_dynamiques'),
    path('api/search-usager-ri2s/', views.api_search_usager_ri2s, name='api_search_usager_ri2s'),
    path('save-beneficiaire/', views.save_beneficiaire, name='save_beneficiaire'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
    path('liste-personnes/', views.liste_personnes_view, name='liste_personnes'),
]

