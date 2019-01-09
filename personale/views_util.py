import datetime
from pprint import pprint as pp

from django.db.models import Q

from personale.models import Anagrafica, Nomine


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
    nr = ng = nv = None

    for azienda in Anagrafica.AZIENDA:

        if ordine == 'cantiere':
            lavoratori = Anagrafica.objects.filter(in_forza=True, azienda=azienda[0]).order_by('-cantiere',
                                                                                               'lavoratore')
            nr = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='r'))
            ng = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='g'))
            nv = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='v'))
        elif ordine == 'stato':
            lavoratori = Anagrafica.objects.filter(in_forza=True, azienda=azienda[0]).filter(
                Q(stato='r') | Q(stato='g')).order_by('-stato', 'lavoratore')
            nr = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='r'))
            ng = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='g'))
        elif ordine == 'idoneita':
            lavoratori = Anagrafica.objects.filter(in_forza=True, azienda=azienda[0]).order_by('idoneita', 'lavoratore')
            nr = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='r'))
            ng = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='g'))
            nv = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='v'))
        else:
            lavoratori = Anagrafica.objects.filter(in_forza=True, azienda=azienda[0]).order_by('lavoratore')
            nr = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='r'))
            ng = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='g'))
            nv = len(Anagrafica.objects.filter(in_forza=True, azienda=azienda[0], stato='v'))

        dati.append((aziende[azienda[0]], lavoratori, (nr, ng, nv)))

    return dati


def lavoratori_con_nomine():
    aziende = {'m': 'MODOMEC',
               'b': 'BUILDING',
               'r': 'RIMEC',
               'w': 'WELDING',
               None: '-'}
    dati = []
    nr = ng = nv = 0

    for azienda in Anagrafica.AZIENDA:
        lavoratori = Nomine.objects.exclude(preposto__isnull=True, antincendio__isnull=True,
                                            primo_soccorso__isnull=True, rls__isnull=True, aspp__isnull=True).order_by(
            'lavoratore')

        llav = []
        for lav in lavoratori:
            xxx = Anagrafica.objects.filter(lavoratore=lav.lavoratore, azienda=azienda[0], in_forza=True)
            if xxx:
                llav.append(xxx[0])
                stato = xxx[0].stato

                if stato == 'v':
                    nv += 1
                elif stato == 'g':
                    ng += 1
                elif stato == 'r':
                    nr += 1

        dati.append((aziende[azienda[0]], llav, (nr, ng, nv)))

    return dati
