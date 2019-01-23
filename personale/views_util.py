import datetime
from pprint import pprint as pp

from django.db.models import Q, Prefetch

from personale.models import Anagrafica, Nomine, Lavoratore


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
            lavoratori = Lavoratore.objects.filter(in_forza=True, azienda=azienda[0]).order_by('-cantiere', 'cognome',
                                                                                               'nome')
        elif ordine == 'stato':
            # lavoratori = Anagrafica.objects.filter(in_forza=True, azienda=azienda[0]).filter(
            #     Q(stato='r') | Q(stato='g')).order_by('-stato', 'lavoratore')

            # todo ora ordina alfabeticamente con anagrafica__stato
            lavoratori = Lavoratore.objects.filter(in_forza=True, azienda=azienda[0]).order_by('-anagrafica__stato',
                                                                                               'cognome',
                                                                                               'nome')
        elif ordine == 'idoneita':
            lavoratori = Lavoratore.objects.filter(in_forza=True, azienda=azienda[0]).order_by('idoneita', 'cognome',
                                                                                               'nome')
        else:
            lavoratori = Lavoratore.objects.filter(in_forza=True, azienda=azienda[0])

        # todo da richiamare lo stato da lavoratore
        n = {'r': len(lavoratori.filter(anagrafica__stato='r')),
             'g': len(lavoratori.filter(anagrafica__stato='g')),
             'v': len(lavoratori.filter(anagrafica__stato='v')),
             't': len(lavoratori)}

        dati.append((aziende[azienda[0]], lavoratori, n))

    return dati


def lavoratori_con_nomine():
    aziende = {'m': 'MODOMEC',
               'b': 'BUILDING',
               'r': 'RIMEC',
               'w': 'WELDING',
               None: '-'}
    dati = []

    for azienda in Anagrafica.AZIENDA:
        lavoratori = Lavoratore.objects.filter(in_forza=True, azienda=azienda[0]).exclude(nomina_preposto__isnull=True,
                                                                                          nomina_antincendio__isnull=True,
                                                                                          nomina_primo_soccorso__isnull=True,
                                                                                          nomina_rls__isnull=True,
                                                                                          nomina_aspp__isnull=True)

        n = {'r': len(lavoratori.filter(anagrafica__stato='r')),
             'g': len(lavoratori.filter(anagrafica__stato='g')),
             'v': len(lavoratori.filter(anagrafica__stato='v')),
             't': len(lavoratori)}

        dati.append((aziende[azienda[0]], lavoratori, n))

    return dati
