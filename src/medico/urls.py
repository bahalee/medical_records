from django.urls import path
from django.views.generic import RedirectView
from .views import (
    home,
    create_medecin,
    create_enregistrement,
    lister_enregistrements,
    effectuer_recherche,
    appliquer_filtres,
    exporter_enregistrement,
    modifier_enregistrement,
    supprimer_enregistrement,
    success
)
from .auth_views import(login_medecin)
from.auth_views import (logout_medecin)
urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='redirect_to_login'), 
    path('login/', login_medecin, name='login'), 
    path('logout/', logout_medecin, name='logout'), 
    path('home/', home, name='home'),  
    path('create_medecin/', create_medecin, name='create_medecin'), 
    path('create_enregistrement/', create_enregistrement, name='create_enregistrement'), 
    path('lister_enregistrements/', lister_enregistrements, name='lister_enregistrements'), 
    path('effectuer_recherche/', effectuer_recherche, name='effectuer_recherche'),  
    path('appliquer_filtres/', appliquer_filtres, name='appliquer_filtres'), 
    path('exporter_enregistrement/<int:idenreg>/<str:format>/', exporter_enregistrement, name='exporter_enregistrement'), 
    path('success/', success, name='success'),  
    path('modifier-enregistrement/<int:pk>/', modifier_enregistrement, name='modifier_enregistrement'),
    path('supprimer_enregistrement/<int:pk>/', supprimer_enregistrement, name='supprimer_enregistrement'),
]