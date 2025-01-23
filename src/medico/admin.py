from django.contrib import admin
from .models import Medecin, Enregistrement

class MedecinAdmin(admin.ModelAdmin):
    list_display = ('email', 'specialite', 'is_active', 'is_staff')
    search_fields = ('email', 'specialite')
    list_filter = ('is_active', 'is_staff')

class EnregistrementAdmin(admin.ModelAdmin):
    list_display = ('nomComplet', 'naissance', 'admission', 'medecin')
    search_fields = ('nomComplet', 'medecin__email', 'medication')
    list_filter = ('medecin', 'naissance', 'admission')

admin.site.register(Medecin, MedecinAdmin)
admin.site.register(Enregistrement, EnregistrementAdmin)