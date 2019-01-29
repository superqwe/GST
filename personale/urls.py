from django.urls import path

from . import views

urlpatterns = [
    # /personale/
    path('', views.index, name='index'),

    # /personale/completo/
    path('completo/', views.completo, name='completo'),
    # /personale/in_forza/
    path('completo/<str:filtro>/', views.completo, name='completo'),
    # /personale/in_forza/[a/s/c]/ a: None  s: azienda  c: cantiere
    path('completo/<str:filtro>/<str:ordinamento>', views.completo, name='completo'),

    # /personale/unilav
    path('unilav/', views.unilav, name='unilav'),

    # /personale/estri_dati/
    path('estrai_dati/', views.estrai_dati2, name='estrai_dati2'),

    # /personale/azione/
    # path('azione/', views.azione, name='azione'),

    # /personale/test/
    path('test/', views.test, name='test'),

]
