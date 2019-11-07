from django.urls import path

from . import views

urlpatterns = [
    # /personale/
    path('', views.index, name='index'),

    # /personale/azione/
    # path('azione/', views.azione, name='azione'),

    # /personale/aggiorna_unilav/
    path('aggiorna_unilav/', views.aggiorna_unilav, name='aggiorna_unilav'),

    # /personale/completo/
    path('completo/', views.completo, name='completo'),
    # /personale/in_forza/
    path('completo/<str:filtro>/', views.completo, name='completo'),
    # /personale/in_forza/[a/s/c]/ a: None  s: azienda  c: cantiere
    path('completo/<str:filtro>/<str:ordinamento>', views.completo, name='completo'),

    # /personale/estri_dati/
    path('estrai_dati/', views.estrai_dati2, name='estrai_dati2'),

    # /personale/estri_dati2/
    path('estrai_dati2/', views.estrai_dati, name='estrai_dati'),
    path('estrai_dati2/estratti/', views.dati_estratti, name='estratti'),

    # /personale/formazione/
    path('formazione/', views.formazione, name='formazione'),

    # /personale/mansioni/
    path('mansioni/', views.mansioni, name='mansioni'),

    # /personale/rait
    path('rait/', views.rait, name='rait'),
    path('rait/estratti/', views.rait_estratti, name='rait_estratti'),

    # /personale/unilav
    path('unilav/', views.unilav, name='unilav'),

    # /personale/test/
    path('test/', views.test, name='test'),

]
