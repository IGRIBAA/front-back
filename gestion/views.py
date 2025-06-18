from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt  # ✅ à ne pas oublier
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_GET
from .models import CibleExperimentation
from django.http import JsonResponse
from .models import CibleExperimentation, StatutCible
from django.shortcuts import render
from .models import ExperimentationGenerale
from django.urls import reverse
from django.http import JsonResponse
from django.http import JsonResponse
from .models import Beneficiaire
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from .models import UsagerPro, UsagerRI2S
from django.shortcuts import render
from rest_framework.generics import UpdateAPIView
from django.shortcuts import get_object_or_404
from .models import Beneficiaire
from django.urls import reverse
from .models import UsagerRI2S
from django.http import JsonResponse
from .models import CibleExperimentation, StatutCible, ChampStatut
from rest_framework.generics import RetrieveAPIView
from .models import Beneficiaire
from urllib.parse import quote
from .models import UsagerRI2S

from .models import ContactReferent

from .serializers import BeneficiaireSerializer

from django.http import HttpResponse
from .models import ExperimentationGenerale
from .models import UsagerPro
from django.views.decorators.csrf import csrf_exempt
import json

def menu_view(request):
    return render(request, 'menu.html')


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import (
    ContactReferent, ExperimentationGenerale, ChampPersonnalise
)

@csrf_exempt
def create_experimentation(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)

        print("---- Données reçues dans POST ----")
        for key in request.POST:
            print(f"{key} => {request.POST.getlist(key)}")

        # 1. Création du contact
        contact = ContactReferent.objects.create(
            nom=request.POST.get('contactNom', ''),
            email=request.POST.get('contactEmail', ''),
            telephone=request.POST.get('contactTel', ''),
        )
        print("✅ Contact créé :", contact)

        # 2. Création de l'expérimentation
        experimentation = ExperimentationGenerale.objects.create(
            nom=request.POST.get('nom', ''),
            entreprise=request.POST.get('entreprise', ''),
            date_debut=request.POST.get('date_debut', None),
            date_fin=request.POST.get('date_fin', None) or None,
            remarques=request.POST.get('remarques', ''),
            contact=contact
        )
        print("✅ Expérimentation créée :", experimentation)

        # ✅ 3. Traitement des SECTIONS personnalisées (titre + champs)
        i = 0
        while True:
            titre = request.POST.get(f'sections[{i}][titre]')
            if not titre:
                break  # Fin des sections

            # Tu vas récupérer tous les noms, types et valeurs possibles de cette section
            noms = request.POST.getlist(f'sections[{i}][champs][]')
            types = request.POST.getlist(f'sections[{i}][types][]')
            valeurs_possibles = request.POST.getlist(f'sections[{i}][valeurs][]')

            for nom, type_, valeurs in zip(noms, types, valeurs_possibles):
                ChampPersonnalise.objects.create(
                    experimentation=experimentation,
                    nom_champ=nom,
                    type_champ=type_,
                    valeurs_possibles=valeurs or ''
                )

            i += 1



        # 4. (Optionnel) Ajout d’autres traitements (cohortes, cibles, statuts…)
        i = 0
        while True:
            titre = request.POST.get(f'sections[{i}][titre]')
            if not titre:
                break  # fin des sections

            champs = request.POST.getlist(f'sections[{i}][champs][]')
            types = request.POST.getlist(f'sections[{i}][types][]')
            valeurs_dyn = request.POST.getlist(f'sections[{i}][valeurs_dyn][]')

            for j, nom_champ in enumerate(champs):
                type_champ = types[j] if j < len(types) else "text"
                valeurs_dyn_source = valeurs_dyn[j] if j < len(valeurs_dyn) else ""

                valeurs_possibles = ""

                if type_champ == "select":
                    # Cherche toutes les options manuelles envoyées sous la forme sections[i][valeurs_manuelles_champid][]
                    champ_id_prefix = f'sections[{i}][valeurs_manuelles_'
                    matching_keys = [key for key in request.POST.keys() if key.startswith(champ_id_prefix)]
                    valeurs_manuelles = []

                    for key in matching_keys:
                        valeurs_manuelles += request.POST.getlist(key)

                    if valeurs_manuelles:
                        valeurs_possibles = ",".join(valeurs_manuelles)
                    elif valeurs_dyn_source:
                        valeurs_possibles = valeurs_dyn_source  # ex: "cohortes", "aidants", etc.

                # Création du champ personnalisé
                ChampPersonnalise.objects.create(
                    experimentation=experimentation,
                    nom_champ=nom_champ,
                    type_champ=type_champ,
                    valeurs_possibles=valeurs_possibles
                )

            i += 1

            # 5. Traitement des cibles et statuts avec champs dynamiques
            for key in request.POST.keys():
                if key.startswith("statuts_"):
                    cible = key.replace("statuts_", "").replace("[]", "")
                    noms_statuts = request.POST.getlist(f"statuts_{cible}[]")

                    for statut_index, nom_statut in enumerate(noms_statuts):
                        sc = StatutCible.objects.create(
                            cible=CibleExperimentation.objects.create(experimentation=experimentation, type_cible=cible),
                            nom_statut=nom_statut
                        )

                        champ_index = 0
                        while True:
                            prefix = f'champs_statut_{cible}_{statut_index}[{champ_index}]'
                            nom_champ = request.POST.get(f'{prefix}[nom]')
                            if not nom_champ:
                                break

                            type_champ = request.POST.get(f'{prefix}[type]', 'text')
                            source_type = request.POST.get(f'{prefix}[source_type]', 'manual')

                            if source_type == 'manual':
                                options = request.POST.getlist(f'{prefix}[options][]')
                                valeurs = ','.join(options)
                            elif source_type in ['cohortes', 'aidants', 'usagers_pro']:
                                valeurs = f'__SOURCE__:{source_type}'
                            else:
                                valeurs = ''

                            ChampStatut.objects.create(
                                statut=sc,
                                nom_champ=nom_champ,
                                type_champ=type_champ,
                                valeurs_possibles=valeurs
                            )
                            champ_index += 1

        return JsonResponse({'success': True, 'redirect_url': '/menu/'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def liste_experimentations_view(request):
    experimentations = ExperimentationGenerale.objects.all().order_by('-date_debut')
    return render(request, 'liste_experimentations.html', {'experimentations': experimentations})


def experimentation_detail_view(request, pk):
    experimentation = get_object_or_404(ExperimentationGenerale, pk=pk)
    return render(request, 'experiment_detail.html', {'experimentation': experimentation})



def form_view(request):
    return render(request, 'Formulaire_Coordinatrice.html')  # ou le nom de ton vrai template

def confirmation_view(request):
    message = request.GET.get("message", "Opération réussie.")
    return render(request, 'confirmation.html', {'message': message})



def save_beneficiaire(request):
    return HttpResponse("Fonction save_beneficiaire à implémenter.")

def experimentation_form_view(request):
    return render(request, 'Formulaire_Expérimentation.html')

def usePro_Form_View(request):
    return render(request, 'Formulaire_Coordinatrice.html')  # ou le bon nom de ton template



def add_usager_pro(request):
    return render(request, 'Formulaire_Coordinatrice.html')  # adapte le nom du template si besoin



class BeneficiaireDetailView(RetrieveAPIView):
    queryset = Beneficiaire.objects.all()
    serializer_class = BeneficiaireSerializer



class BeneficiaireUpdateView(UpdateAPIView):
    queryset = Beneficiaire.objects.all()
    serializer_class = BeneficiaireSerializer



def beneficiaire_detail_view(request, pk):
    beneficiaire = get_object_or_404(Beneficiaire, pk=pk)
    return render(request, 'beneficiaire_detail.html', {'beneficiaire': beneficiaire})




def get_statuts_champs(request):
    experimentation_id = request.GET.get("experimentation_id")
    cible_type = request.GET.get("cible")

    try:
        cible = CibleExperimentation.objects.get(experimentation_id=experimentation_id, type_cible=cible_type)
        statuts = StatutCible.objects.filter(cible=cible)
        data = []

        for statut in statuts:
            champs = ChampStatut.objects.filter(statut=statut).values_list('nom_champ', flat=True)
            data.append({
                "nom_statut": statut.nom_statut,
                "champs": list(champs)
            })

        return JsonResponse({"success": True, "statuts": data})
    except CibleExperimentation.DoesNotExist:
        return JsonResponse({"success": False, "error": "Cible non trouvée"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})



def ajouter_beneficiaire_view(request):
    experimentations = ExperimentationGenerale.objects.all()
    return render(request, 'Formulaire_Coordinatrice.html', {
        'experimentations': experimentations
    })




def api_statuts_champs(request):
    experimentation_id = request.GET.get("experimentation_id")
    cible = request.GET.get("cible")

    try:
        cible_obj = CibleExperimentation.objects.get(
            experimentation_id=experimentation_id,
            type_cible=cible
        )
        statuts = cible_obj.statuts.prefetch_related("champs")
        resultat = []
        for statut in statuts:
            resultat.append({
                "nom_statut": statut.nom_statut,
                "champs": [c.nom_champ for c in statut.champs.all()]
            })
        return JsonResponse({"success": True, "statuts": resultat})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})




@require_GET
def api_cibles_experimentation(request):
    experimentation_id = request.GET.get("experimentation_id")

    if not experimentation_id:
        return JsonResponse({"success": False, "error": "ID manquant"})

    cibles = CibleExperimentation.objects.filter(experimentation_id=experimentation_id)
    data = [c.type_cible for c in cibles]

    return JsonResponse({"success": True, "cibles": data})


def api_usagers_par_statut(request):
    statut = request.GET.get("statut")

    try:
        if not statut:
            return JsonResponse({'success': False, 'error': 'Statut non spécifié'})

        beneficiaires = Beneficiaire.objects.filter(statut=statut)  # adapte selon ton modèle
        data = [
            {
                'id': b.id,
                'nom': b.nom,
                'prenom': b.prenom
            }
            for b in beneficiaires
        ]

        return JsonResponse({'success': True, 'usagers': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



@csrf_exempt
def ajouter_usager_pro(request):
    if request.method == 'POST':
        UsagerPro.objects.create(
            nom=request.POST.get('nom'),
            email=request.POST.get('email'),
            cible=request.POST.get('cible')
        )
        return redirect('gestion:confirmation')  # ou ta page de redirection
    return render(request, 'ajouter_usager_pro.html')

def api_usagers_pro(request):
    cible = request.GET.get("cible")
    usagers = UsagerPro.objects.filter(cible=cible).values("id", "nom", "email")
    return JsonResponse({"success": True, "usagers": list(usagers)})






def ajouter_usager_ri2s(request):
    if request.method == 'POST':
        type_usager = request.POST.get('type_usager')

        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        sexe = request.POST.get('sexe')

        if type_usager == 'pro':
            profession = request.POST.get('profession')
            structure = request.POST.get('structure')

            UsagerPro.objects.create(
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                email=email,
                profession=profession,
                structure=structure,
                sexe=sexe
            )
        else:
            date_naissance = request.POST.get('date_naissance')
            code_postal = request.POST.get('code_postal')

            UsagerRI2S.objects.create(
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                email=email,
                date_naissance=date_naissance,
                code_postal=code_postal,
                sexe=sexe
            )

        # ✅ Redirection propre après POST réussi
        return redirect('gestion:menu')

    # GET : affiche le bon formulaire
    return render(request, 'ajouter_usager_ri2s.html')






