import datetime

from django.http import HttpResponse
from django.template import loader

from personale.models import Lavoratore


def index(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")


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
    lavoratori = Lavoratore.objects.order_by('cognome', 'nome')

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
