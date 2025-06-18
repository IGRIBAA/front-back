from django.contrib import admin
from .models import Beneficiaire, Aidant, Experimentation, Fichier
from .models import UsagerPro, UsagerRI2S 
admin.site.register(Beneficiaire)
admin.site.register(Aidant)
admin.site.register(Experimentation)
admin.site.register(Fichier)
admin.site.register(UsagerRI2S)
admin.site.register(UsagerPro)