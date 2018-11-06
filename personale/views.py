import datetime

from django.http import HttpResponse
from django.template import loader

from personale.models import Lavoratore, Formazione, Anagrafica
from personale.views_util import date_scadenza

from pprint import pprint as pp

def index(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")


def anagrafica(request):
    lavoratori = Anagrafica.objects.order_by('lavoratore')
    cantieri = Anagrafica.CANTIERE

    dati = []
    for cantiere in cantieri:
        lavoratori = Anagrafica.objects.filter(cantiere=cantiere[0]).order_by('lavoratore')

        dati.append((cantiere[1], lavoratori))


    template = loader.get_template('personale/anagrafica_per_cantiere.html')
    context = {
        'lavoratori': lavoratori,
        'lavoratori_per_cantiere': dati,
        'oggi': date_scadenza()['oggi'],
        'mesi1': date_scadenza()['mesi1'],
        'mesi2': date_scadenza()['mesi2'],
        'mesi6': date_scadenza()['mesi6'],
        'mesi12': date_scadenza()['mesi12'],
    }
    return HttpResponse(template.render(context, request))


def completo(request):
    lavoratori = Lavoratore.objects.order_by('cognome', 'nome')

    oggi = datetime.date.today()
    mesi1 = oggi + datetime.timedelta(days=30)
    mesi2 = oggi + datetime.timedelta(days=60)
    mesi6 = oggi + datetime.timedelta(days=366 / 2)
    mesi12 = oggi + datetime.timedelta(days=365)

    template = loader.get_template('personale/completo.html')
    context = {
        'lavoratori': lavoratori,
        'oggi': oggi,
        'mesi1': mesi1,
        'mesi2': mesi2,
        'mesi6': mesi6,
        'mesi12': mesi12,
    }
    return HttpResponse(template.render(context, request))


def formazione(request):
    lavoratori = Formazione.objects.order_by('lavoratore')

    oggi = datetime.date.today()
    mesi1 = oggi + datetime.timedelta(days=30)
    mesi2 = oggi + datetime.timedelta(days=60)
    mesi6 = oggi + datetime.timedelta(days=366 / 2)
    mesi12 = oggi + datetime.timedelta(days=365)

    template = loader.get_template('personale/formazione.html')
    context = {
        'lavoratori': lavoratori,
        'oggi': oggi,
        'mesi1': mesi1,
        'mesi2': mesi2,
        'mesi6': mesi6,
        'mesi12': mesi12,
    }
    return HttpResponse(template.render(context, request))


def scadenza(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")
