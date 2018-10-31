from django.urls import path

from . import views

urlpatterns = [
    # /personale/
    path('', views.index, name='index'),
    # /personale/globale/
    path('globale/', views.globale, name='globale'),
    # /personale/scadenza/
    path('scadenza/', views.scadenza, name='scadenza'),
    # /personale/formazione/
    path('formazione/', views.formazione, name='formazione'),
]