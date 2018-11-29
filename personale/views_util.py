import datetime
from pprint import pprint as pp

from django.db.models import Q

from personale.models import Anagrafica


def date_scadenza():
    oggi = datetime.date.today()
    mesi1 = oggi + datetime.timedelta(days=30)
    mesi2 = oggi + datetime.timedelta(days=60)
    mesi6 = oggi + datetime.timedelta(days=366 / 2)
    mesi12 = oggi + datetime.timedelta(days=365)

    return {'oggi': oggi,
            'mesi1': mesi1,
            'mesi2': mesi2,
            'mesi6': mesi6,
            'mesi12': mesi12
            }


class Date_Scadenza():
    def __init__(self):
        self.oggi = datetime.date.today()
        self.mesi1 = self.oggi + datetime.timedelta(days=30)
        self.mesi2 = self.oggi + datetime.timedelta(days=60)
        self.mesi6 = self.oggi + datetime.timedelta(days=366 / 2)
        self.mesi12 = self.oggi + datetime.timedelta(days=365)


def lavoratori_suddivisi_per_azienda(ordine=None):
    aziende = {'m': 'MODOMEC',
               'b': 'BUILDING',
               'r': 'RIMEC',
               'w': 'WELDING',
               None: '-'}
    dati = []

    for azienda in Anagrafica.AZIENDA:

        if ordine == 'cantiere':
            lavoratori = Anagrafica.objects.filter(in_forza=True, azienda=azienda[0]).order_by('-cantiere',
                                                                                               'lavoratore')
        elif ordine == 'stato':
            lavoratori = Anagrafica.objects.filter(in_forza=True, azienda=azienda[0]).filter(
                Q(stato='r') | Q(stato='g')).order_by('-stato', 'lavoratore')
        elif ordine == 'idoneita':
            lavoratori = Anagrafica.objects.filter(in_forza=True, azienda=azienda[0]).order_by('idoneita')
        else:
            lavoratori = Anagrafica.objects.filter(in_forza=True, azienda=azienda[0]).order_by('lavoratore')

        dati.append((aziende[azienda[0]], lavoratori))

    return dati
