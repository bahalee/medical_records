from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Medecin, Enregistrement

class MedecinAdmin(UserAdmin):
    list_display = ('email', 'nom_complet', 'specialite', 'is_active', 'is_staff')
    search_fields = ('email', 'nom_complet', 'specialite')
    list_filter = ('is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('nom_complet', 'specialite', 'medico')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom_complet', 'specialite', 'medico', 'password1', 'password2')}
        ),
    )

    ordering = ('email',)

class EnregistrementAdmin(admin.ModelAdmin):
    list_display = ('nomComplet', 'naissance', 'admission', 'medecin')
    search_fields = ('nomComplet', 'medecin__email', 'medication')
    list_filter = ('medecin', 'naissance', 'admission')

admin.site.register(Medecin, MedecinAdmin)
admin.site.register(Enregistrement, EnregistrementAdmin)