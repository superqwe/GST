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
    nv = None

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


def lavoratori_suddivisi_per_azienda2(ordine=None):
    aziende = {'m': 'MODOMEC',
               'b': 'BUILDING',
               'r': 'RIMEC',
               'w': 'WELDING',
               None: '-'}
    dati = []

    for azienda in Anagrafica.AZIENDA:

        if ordine == 'cantiere':
            lavoratori = Lavoratore.objects.all().prefetch_related(
                'anagrafica_set', 'formazione_set', 'nomine_set'
            ).filter(
                anagrafica__in_forza=True, anagrafica__azienda=azienda[0]
            ).order_by(
                '-anagrafica__cantiere', 'cognome', 'nome'
            )
        elif ordine == 'stato':
            # lavoratori = Anagrafica.objects.filter(in_forza=True, azienda=azienda[0]).filter(
            #     Q(stato='r') | Q(stato='g')).order_by('-stato', 'lavoratore')

            # todo ora ordina alfabeticamente con anagrafica__stato
            lavoratori = Lavoratore.objects.all().prefetch_related(
                'anagrafica_set', 'formazione_set', 'nomine_set'
            ).filter(
                anagrafica__in_forza=True, anagrafica__azienda=azienda[0]
            ).order_by(
                '-anagrafica__stato', 'cognome', 'nome'
            )
        elif ordine == 'idoneita':
            lavoratori = Lavoratore.objects.all().prefetch_related(
                'anagrafica_set', 'formazione_set', 'nomine_set'
            ).filter(
                anagrafica__in_forza=True, anagrafica__azienda=azienda[0]
            ).order_by(
                'anagrafica__idoneita', 'cognome', 'nome'
            )
        else:
            lavoratori = Lavoratore.objects.all().prefetch_related('anagrafica_set', 'formazione_set',
                                                                   'nomine_set').filter(anagrafica__in_forza=True,
                                                                                        anagrafica__azienda=azienda[0])
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
        lavoratori = Lavoratore.objects.all().prefetch_related(
            'anagrafica_set', 'formazione_set', 'nomine_set'
        ).filter(
            anagrafica__in_forza=True, anagrafica__azienda=azienda[0]
        ).exclude(nomine__preposto__isnull=True, nomine__antincendio__isnull=True,
                  nomine__primo_soccorso__isnull=True, nomine__rls__isnull=True, nomine__aspp__isnull=True)

        n = {'r': len(lavoratori.filter(anagrafica__stato='r')),
             'g': len(lavoratori.filter(anagrafica__stato='g')),
             'v': len(lavoratori.filter(anagrafica__stato='v')),
             't': len(lavoratori)}

        dati.append((aziende[azienda[0]], lavoratori, n))

    return dati
