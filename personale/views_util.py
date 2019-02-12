import datetime

from django.db.models import Q

from personale.models import Lavoratore, Azienda, Cantiere

AZIENDE = ('Modomec', 'Building', 'Rimec', 'Welding', '-')


def autorizzato(user):
    return user.is_superuser or ('utente_modomec',) in user.groups.all().values_list('name')


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


def lavoratori_suddivisi_per_azienda(ordine=None, in_forza=True):
    dati = []

    for azienda in AZIENDE:
        azienda = Azienda.objects.get(nome=azienda)

        if ordine == 'cantiere':
            lavoratori = Lavoratore.objects.filter(in_forza=in_forza, azienda=azienda).order_by('-cantiere', 'cognome',
                                                                                                'nome')
        elif ordine == 'arcelormittal':
            lavoratori = Lavoratore.objects.filter(in_forza=in_forza, azienda=azienda, cantiere=Cantiere.objects.get(
                nome='ArcelorMittal')).filter().order_by('cognome', 'nome')

        elif ordine == 'stato':
            lavoratori = Lavoratore.objects.filter(in_forza=in_forza, azienda=azienda).filter(
                Q(stato='r') | Q(stato='g')).order_by('stato', 'cognome', 'nome')

        elif ordine == 'idoneita':
            lavoratori = Lavoratore.objects \
                .filter(in_forza=in_forza, azienda=azienda) \
                .order_by('idoneita', 'cognome', 'nome') \
                .exclude(
                Q(cantiere=Cantiere.objects.get(nome='Marghera')) | Q(cantiere=Cantiere.objects.get(nome='Monfalcone')))
        else:
            lavoratori = Lavoratore.objects.filter(in_forza=in_forza, azienda=azienda)

        n = {'r': len(lavoratori.filter(stato='r')),
             'g': len(lavoratori.filter(stato='g')),
             'v': len(lavoratori.filter(stato='v')),
             't': len(lavoratori)}

        if n['t']:
            dati.append((azienda, lavoratori, n))

    return dati


def lavoratori_con_nomine():
    dati = []

    for azienda in AZIENDE:
        azienda = Azienda.objects.get(nome=azienda)
        lavoratori = Lavoratore.objects.filter(in_forza=True, azienda=azienda).exclude(nomina_preposto__isnull=True,
                                                                                       nomina_antincendio__isnull=True,
                                                                                       nomina_primo_soccorso__isnull=True,
                                                                                       nomina_rls__isnull=True,
                                                                                       nomina_aspp__isnull=True)

        n = {'r': len(lavoratori.filter(stato='r')),
             'g': len(lavoratori.filter(stato='g')),
             'v': len(lavoratori.filter(stato='v')),
             't': len(lavoratori)}

        if n['t']:
            dati.append((azienda, lavoratori, n))

    return dati
