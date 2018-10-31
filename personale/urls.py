from django.urls import path

from . import views

urlpatterns = [
    # /personale/
    path('', views.index, name='index'),

    # /personale/completo/
    path('completo/', views.completo, name='completo'),

    # /personale/formazione/
    path('formazione/', views.formazione, name='formazione'),

    # /personale/scadenza/
    path('scadenza/', views.scadenza, name='scadenza'),
]