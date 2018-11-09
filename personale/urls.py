from django.urls import path

from . import views

urlpatterns = [
    # /personale/
    path('', views.index, name='index'),

    # /personale/anagrafica/
    path('anagrafica/', views.anagrafica, name='anagrafica'),
    # /personale/anagrafica_per_cantiere/
    path('anagrafica_per_cantiere/', views.anagrafica_per_cantiere, name='anagrafica_per_cantiere'),

    # /personale/completo/
    path('completo/', views.completo, name='completo'),
    # /personale/in_forza/
    path('completo/<str:filtro>/', views.completo, name='completo'),

    # /personale/formazione/
    path('formazione/', views.formazione, name='formazione'),

    # /personale/scadenza/
    path('scadenza/', views.scadenza, name='scadenza'),

    # /personale/estri_dati/
    path('estrai_dati/', views.estrai_dati, name='estrai_dati'),

    # # /personale/azione/
    # path('azione/', views.azione, name='azione'),

]