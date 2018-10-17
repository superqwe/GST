from django.http import HttpResponse
from django.template import loader

from personale.models import Lavoratore


def index(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")


def globale(request):
    lavoratori = Lavoratore.objects.order_by('cognome', 'nome')

    template = loader.get_template('personale/index.html')
    context = {
        'lavoratori': lavoratori,
    }
    return HttpResponse(template.render(context, request))


def scadenza(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")
