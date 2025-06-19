# models.py propre et corrigé
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

# -------------------------
# USAGERS / AIDANTS / BÉNÉFICIAIRES
# -------------------------
class Beneficiaire(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1)
    code_postal = models.CharField(max_length=10)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"




class Aidant(models.Model):
    beneficiaire = models.ForeignKey(Beneficiaire, related_name='aidants', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    telephone = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', message="Le numéro doit contenir exactement 10 chiffres.")]
    )
    lien_parente = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.lien_parente})"


# -------------------------
# EXPÉRIMENTATION GÉNÉRALE / STRUCTURE
# -------------------------
class ContactReferent(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=10)

    def __str__(self):
        return self.nom

class ExperimentationGenerale(models.Model):
    nom = models.CharField(max_length=255)
    entreprise = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    remarques = models.TextField(blank=True)
    contact = models.OneToOneField(ContactReferent, on_delete=models.CASCADE, related_name='experimentation_generale')

    def __str__(self):
        return self.nom

class Cohorte(models.Model):
    experimentation = models.ForeignKey(ExperimentationGenerale, on_delete=models.CASCADE, related_name='cohortes')
    nom = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.experimentation.nom})"


# -------------------------
# CHAMPS PERSONNALISÉS GÉNÉRAUX
# -------------------------
class ChampPersonnalise(models.Model):
    TYPE_CHOIX = [
        ('text', 'Texte'),
        ('date', 'Date'),
        ('number', 'Nombre'),
        ('file', 'Fichier'),
        ('select', 'Liste déroulante'),
    ]
    experimentation = models.ForeignKey(ExperimentationGenerale, on_delete=models.CASCADE, related_name='champs_perso')
    titre_section = models.CharField(max_length=255, default="")
    nom_champ = models.CharField(max_length=255)
    type_champ = models.CharField(max_length=20, choices=TYPE_CHOIX)
    valeurs_possibles = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nom_champ} ({self.type_champ})"


# -------------------------
# CIBLES / STATUTS / CHAMPS PAR STATUT
# -------------------------
class CibleExperimentation(models.Model):
    CIBLES = [
        ('seniors', 'Seniors'),
        ('professionnels', 'Professionnels'),
        ('aidants', 'Aidants'),
    ]
    experimentation = models.ForeignKey(ExperimentationGenerale, on_delete=models.CASCADE, related_name='cibles')
    type_cible = models.CharField(max_length=20, choices=CIBLES)

    def __str__(self):
        return f"{self.get_type_cible_display()} - {self.experimentation.nom}"

class StatutCible(models.Model):
    cible = models.ForeignKey(CibleExperimentation, on_delete=models.CASCADE, related_name='statuts')
    nom_statut = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom_statut} ({self.cible.type_cible} - {self.cible.experimentation.nom})"

class ChampStatut(models.Model):
    statut = models.ForeignKey(StatutCible, on_delete=models.CASCADE, related_name='champs')
    section = models.CharField(max_length=255, default="")  # Titre section
    nom_champ = models.CharField(max_length=255)
    type_champ = models.CharField(max_length=50)
    valeurs_possibles = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nom_champ} (Statut: {self.statut.nom_statut})"


# -------------------------
# USAGERS PRO / RI2S
# -------------------------
class UsagerPro(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)  # au lieu de 10
    email = models.EmailField(max_length=255, blank=True)  # explicite
    profession = models.CharField(max_length=100)
    structure = models.CharField(max_length=100)
    remarques = models.TextField(blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

    cible = models.CharField(
        max_length=30,
        choices=[
            ('seniors', 'Seniors'),
            ('aidants', 'Aidants'),
            ('professionnels', 'Professionnels')
        ],
        default='seniors'
    )

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.profession}"

class UsagerRI2S(models.Model):
    TYPE_CHOICES = [
        ('pro', 'Professionnel'),
        ('non_pro', 'Non professionnel'),
    ]
    type_usager = models.CharField(max_length=10, choices=TYPE_CHOICES)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    role = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    sexe = models.CharField(max_length=10)
    date_naissance = models.DateField(null=True, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    structure = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


# -------------------------
# FICHIERS EXPÉRIMENTATIONS
# -------------------------
class Experimentation(models.Model):
    TYPE_CHOICES = [
        ('TelegrafiK', 'TelegrafiK'),
        ('Presage', 'Presage'),
    ]
    STATUT_CHOICES = [
        ('noninitie', 'Non initié'),
        ('visite', 'Visite programmée'),
        ('consentement', 'Consentement signé'),
        ('consentementTGK', 'Consentement signé (TelegrafiK)'),
        ('installation', 'Installation programmée'),
        ('actif', 'Actif'),
        ('interrompu', 'Interrompu'),
        ('fini', 'Fini'),
        ('desinstalle', 'Désinstallé'),
    ]
    METHODE_RECRUTEMENT_CHOICES = [
        ('evenement', 'Événement'),
        ('partenaire', 'Partenaire'),
        ('usager', 'Usager pro'),
    ]
    beneficiaire = models.ForeignKey(Beneficiaire, related_name='experimentations', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    coordinateur = models.CharField(max_length=100)
    cohorte = models.CharField(max_length=100)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    adresse_domicile = models.TextField(blank=True)
    methode_recrutement = models.CharField(max_length=20, choices=METHODE_RECRUTEMENT_CHOICES, blank=True)
    detail_recrutement = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.type} - {self.get_statut_display()}"

class Fichier(models.Model):
    TYPE_CHOICES = [
        ('formulaire_ri2s', 'Formulaire RI2S'),
        ('consentement_telegrafik', 'Consentement TELEGRAFIK'),
        ('bon_installation', "Bon d'installation"),
        ('consentement_ri2s', 'Consentement RI2S'),
    ]
    experimentation = models.ForeignKey(Experimentation, related_name='fichiers', on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='uploads/%Y/%m/%d/')
    type_fichier = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.get_type_fichier_display()} - {self.experimentation}"

class ChampCommun(models.Model):
    experimentation = models.ForeignKey(ExperimentationGenerale, related_name="champs_communs", on_delete=models.CASCADE)
    titre_section = models.CharField(max_length=255, default="Section commune")
    nom_champ = models.CharField(max_length=255)
    type_champ = models.CharField(max_length=50, choices=[
        ('text', 'Texte'),
        ('date', 'Date'),
        ('number', 'Nombre'),
        ('file', 'Fichier'),
        ('select', 'Liste déroulante'),
    ])
    valeurs_possibles = models.TextField(blank=True)

    def __str__(self):
        return f"[COMMUN] {self.titre_section} - {self.nom_champ} ({self.type_champ})"

class BeneficiaireExperimentation(models.Model):
    usager = models.ForeignKey(UsagerRI2S, on_delete=models.CASCADE)
    experimentation = models.ForeignKey(ExperimentationGenerale, on_delete=models.CASCADE)
    cible = models.CharField(max_length=50)
    statut = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.usager.nom} {self.usager.prenom} - {self.experimentation.nom} ({self.cible})"