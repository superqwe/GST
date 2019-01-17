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
    # /personale/in_forza/[a/s/c]/ a: None  s: azienda  c: cantiere
    path('completo/<str:filtro>/<str:ordinamento>', views.completo, name='completo'),

    # /personale/formazione/
    path('formazione/', views.formazione, name='formazione'),

    # /personale/scadenza/
    path('scadenza/', views.scadenza, name='scadenza'),

    # /personale/unilav
    path('unilav/', views.unilav, name='unilav'),

    # /personale/estri_dati/
    path('estrai_dati/', views.estrai_dati, name='estrai_dati'),

    # # /personale/azione/
    # path('azione/', views.azione, name='azione'),

    # /personale/pdf/
    path('pdf/', views.esporta_pdf, name='esporta_pdf'),

    # /personale/test/
    path('test/', views.test, name='test'),

]
