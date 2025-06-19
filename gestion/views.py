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
from django.views.decorators.http import require_GET
from .models import UsagerRI2S
from django.http import JsonResponse
from .models import BeneficiaireExperimentation 

from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import ContactReferent
from django.shortcuts import get_object_or_404, redirect
from .models import UsagerRI2S, ExperimentationGenerale, BeneficiaireExperimentation

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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import (
    ContactReferent, ExperimentationGenerale, ChampPersonnalise,
    ChampCommun, CibleExperimentation, StatutCible, ChampStatut
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

        # 2. Création de l'expérimentation
        experimentation = ExperimentationGenerale.objects.create(
            nom=request.POST.get('nom', ''),
            entreprise=request.POST.get('entreprise', ''),
            date_debut=request.POST.get('date_debut', None),
            date_fin=request.POST.get('date_fin', None) or None,
            remarques=request.POST.get('remarques', ''),
            contact=contact
        )

        # 3. Champs communs (titre + champ)
        titres = request.POST.getlist('titre_section[]')
        noms = request.POST.getlist('nom_champ[]')
        types = request.POST.getlist('type_champ[]')
        valeurs = request.POST.getlist('valeurs_possibles[]')
        source_types = request.POST.getlist('source_type_champ[]')

        for i in range(len(noms)):
            type_champ = types[i]
            source_type = source_types[i] if i < len(source_types) else 'manual'

            if type_champ == 'select':
                if source_type == 'manual':
                    valeurs_possibles = valeurs[i]
                else:
                    valeurs_possibles = f"__SOURCE__:{source_type}"
            else:
                valeurs_possibles = ""

            ChampCommun.objects.create(
                experimentation=experimentation,
                titre_section=titres[i] if i < len(titres) else "",
                nom_champ=noms[i],
                type_champ=type_champ,
                valeurs_possibles=valeurs_possibles
            )
        print("------ DONNÉES FORMULAIRE POST ------")
        for key, value in request.POST.items():
            print(f"{key} : {value}")



        # 4. Statuts et champs par cible
        for key in request.POST.keys():
            if key.startswith("statuts_"):
                cible = key.replace("statuts_", "").replace("[]", "")
                noms_statuts = request.POST.getlist(f"statuts_{cible}[]")

                cible_obj = CibleExperimentation.objects.create(
                    experimentation=experimentation,
                    type_cible=cible
                )

                for index, nom_statut in enumerate(noms_statuts):
                    sc = StatutCible.objects.create(
                        cible=cible_obj,
                        nom_statut=nom_statut
                    )

                    noms = request.POST.getlist(f'champs_statut_{cible}_{index}[noms][]')
                    types = request.POST.getlist(f'champs_statut_{cible}_{index}[types][]')
                    source_types = request.POST.getlist(f'champs_statut_{cible}_{index}[source_type][]')
                    champ_ids = request.POST.getlist(f'champs_statut_{cible}_{index}[champ_ids][]')

                    for j, nom_champ in enumerate(noms):
                        type_champ = types[j] if j < len(types) else 'text'
                        source_type = source_types[j] if j < len(source_types) else 'manual'
                        champ_id = champ_ids[j] if j < len(champ_ids) else None
                        valeurs = ''

                        if type_champ == 'select':
                            if source_type == 'manual' and champ_id:
                                options = request.POST.getlist(f'select_options_{champ_id}[]')
                                valeurs = ','.join(options)
                            elif source_type in ['cohortes', 'aidants', 'usagers_pro']:
                                valeurs = f'__SOURCE__:{source_type}'

                        ChampStatut.objects.create(
                            statut=sc,
                            nom_champ=nom_champ,
                            type_champ=type_champ,
                            valeurs_possibles=valeurs
                        )

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
    if request.method == 'POST':
        experimentation_id = request.POST.get("experimentation_id")
        cible = request.POST.get("cible")
        statut_index = request.POST.get("statut")
        usager_id = request.POST.get("usager_id")

        # 1. Récupération des objets nécessaires
        experimentation = get_object_or_404(ExperimentationGenerale, id=experimentation_id)
        usager = get_object_or_404(UsagerRI2S, id=usager_id)

        # 2. Création du lien bénéficiaire - expérimentation
        BeneficiaireExperimentation.objects.create(
            usager=usager,
            experimentation=experimentation,
            cible=cible,
            statut=statut_index
        )

        # 3. Ajout du rôle dynamique si pas encore présent
        nouveau_role = f"bénéficiaire - {experimentation.nom}"
        if nouveau_role not in usager.role:
            usager.role.append(nouveau_role)
            usager.save()

        # 4. Redirection avec message de confirmation
        return redirect(reverse('gestion:confirmation') + "?message=Bénéficiaire ajouté avec succès")

    # Si ce n’est pas un POST, on retourne au menu
    return redirect('gestion:menu')


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
        type_usager = request.POST.get('type_usager')  # 'pro' ou autre

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

            # 💡 Rôle par défaut : 'senior' ou 'aidant'
            role_initial = request.POST.get('role', '')  # Ajoute un champ <select> dans ton formulaire
            roles = [role_initial] if role_initial else []

            UsagerRI2S.objects.create(
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                email=email,
                date_naissance=date_naissance,
                code_postal=code_postal,
                sexe=sexe,
                role=roles
            )

        return redirect('gestion:menu')

    return render(request, 'ajouter_usager_ri2s.html')


@require_GET
def api_options_dynamiques(request):
    source = request.GET.get("source")

    if source == "cohortes":
        data = list(ExperimentationGenerale.objects.values_list("nom", flat=True))
    elif source == "aidants":
        data = list(Beneficiaire.objects.filter(type_usager='aidant').values_list("nom", flat=True))
    elif source == "usagers_pro":
        data = list(UsagerPro.objects.values_list("nom", flat=True))
    else:
        return JsonResponse({"success": False, "error": "Source inconnue"}, status=400)

    return JsonResponse({"success": True, "options": data})



@require_GET
def api_search_usager_ri2s(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"success": True, "usagers": []})
    usagers = UsagerRI2S.objects.filter(
        prenom__icontains=q
    )[:10] | UsagerRI2S.objects.filter(nom__icontains=q)[:10]
    data = [{"id": u.id, "nom": u.nom, "prenom": u.prenom} for u in usagers]
    return JsonResponse({"success": True, "usagers": data})


def liste_personnes_view(request):
    usagers = UsagerRI2S.objects.all()
    return render(request, 'gestion/liste_personnes.html', {'usagers': usagers})
