import datetime
from configparser import ConfigParser
from pprint import pprint as pp

from django.db.models import Q

from personale.models import Lavoratore, Azienda, Cantiere
from personale.views_estrai_dati import Estrai

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


class DateScadenza:
    def __init__(self):
        self.oggi = datetime.date.today()
        self.mesi1 = self.oggi + datetime.timedelta(days=30)
        self.mesi2 = self.oggi + datetime.timedelta(days=60)
        self.mesi6 = self.oggi + datetime.timedelta(days=366 / 2)
        self.mesi12 = self.oggi + datetime.timedelta(days=365)
        self.mesi1prima = self.oggi - datetime.timedelta(days=30)
        self.mesi6prima = self.oggi - datetime.timedelta(days=366 / 2)


def lavoratori_suddivisi_per_azienda(ordine=None, in_forza=True):
    dati = []
    scadenza = DateScadenza()

    for azienda in AZIENDE:
        azienda = Azienda.objects.get(nome=azienda)

        if ordine == 'cantiere':
            lavoratori = Lavoratore.objects.filter(in_forza=in_forza, azienda=azienda).order_by('cantiere', 'cognome',
                                                                                                'nome')
        elif ordine == 'arcelormittal':
            lavoratori = Lavoratore.objects.filter(in_forza=in_forza, azienda=azienda, cantiere=Cantiere.objects.get(
                nome='ArcelorMittal')).filter().order_by('cognome', 'nome')

        elif ordine == 'stato':
            lavoratori = Lavoratore.objects \
                .filter(in_forza=in_forza, azienda=azienda) \
                .filter(Q(stato='r') | Q(stato='g')).order_by('stato', 'cognome', 'nome') \
                .exclude(Q(cantiere=Cantiere.objects.get(nome='Marghera (VE)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Fincantieri (AN)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Fincantieri (GO)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Andritz (CH)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Andritz (DE)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Andritz (NL)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Macchi (VE)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Marioff'))
                         | Q(cantiere=Cantiere.objects.get(nome='-'))
                         | Q(cantiere=Cantiere.objects.get(nome='ArcelorMittal'))
                         | Q(cantiere=Cantiere.objects.get(nome='ISAB (SR)'))
                         )

        elif ordine == 'idoneita':
            lavoratori = Lavoratore.objects \
                .filter(in_forza=in_forza, azienda=azienda) \
                .filter(Q(idoneita__lte=scadenza.mesi2) | Q(idoneita=None)) \
                .order_by('idoneita', 'cognome', 'nome') \
                .exclude(Q(cantiere=Cantiere.objects.get(nome='ArcelorMittal'))
                         | Q(cantiere=Cantiere.objects.get(nome='Andritz (CH)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Andritz (DE)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Andritz (NL)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Ansaldo (VE)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Distacco'))
                         | Q(cantiere=Cantiere.objects.get(nome='Fincantieri (AN)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Fincantieri (GO)'))
                         | Q(cantiere=Cantiere.objects.get(nome='ISAB (SR)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Macchi (VE)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Marghera (VE)'))
                         | Q(cantiere=Cantiere.objects.get(nome='Marioff'))
                         | Q(cantiere=Cantiere.objects.get(nome='-'))
                         )

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
        lavoratori = Lavoratore.objects \
            .filter(in_forza=True, azienda=azienda) \
            .exclude(preposto__isnull=True,
                     dirigente__isnull=True,
                     antincendio__isnull=True,
                     primo_soccorso__isnull=True,
                     rls__isnull=True,
                     nomina_preposto__isnull=True,
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


class EstraiDatiUtil(object):
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read('estrai_dati.txt')
        self.aggiorna_lista_cantieri()

    def leggi_cfg(self):
        """elenco di tutte le preferenze"""

        cfg = {}

        for sec in self.parser.sections():

            for k, v in self.parser.items(sec):
                cfg[k] = 0 if v == '0' else 1

        return cfg

    def organizza_cfg(self):
        """organizza le preferenze per sezioni da inviare alla pagina html"""

        estrazione = {'tipo_estrazione': self.parser.get('estrazione', 'tipo'),
                      'nome_file_xlsx': self.parser.get('estrazione', 'nome_file_xlsx')}

        filtro_impresa = list(((k, True if v == '1' else False) for k, v in self.parser.items('filtro_impresa')))
        filtro_cantiere = list(((k, True if v == '1' else False) for k, v in self.parser.items('filtro_cantiere')))
        filtro_cantiere.sort()

        base = ((k, True if v == '1' else False) for k, v in self.parser.items('base'))
        formazione = ((k, True if v == '1' else False) for k, v in self.parser.items('formazione'))
        nomine = ((k, True if v == '1' else False) for k, v in self.parser.items('nomine'))

        return {'estrazione': estrazione,
                'filtro_impresa': filtro_impresa,
                'filtro_cantiere': filtro_cantiere,
                'documenti': (('Base', base), ('Formazione', formazione), ('Nomine', nomine))}

    def scrivi_cfg(self, post):
        """scrive le preferenze da POST"""

        print('dati post ------------------')
        pp(post)

        for sec in self.parser.sections():

            for k in self.parser.items(sec):
                self.parser.set(sec, k[0], '0')

        for k in post:

            for sec in self.parser.sections():

                if self.parser.has_option(sec, k):
                    self.parser.set(sec, k, '1')

        self.parser.set('estrazione', 'tipo', post['tipo_estrazione'])

        if 'nome_file_xlsx' in post:
            self.parser.set('estrazione', 'nome_file_xlsx', post['nome_file_xlsx'])

        with open('estrai_dati.txt', 'w') as configfile:
            self.parser.write(configfile)

    def estrai_documenti(self, post=False):
        preferenze = self.organizza_cfg()

        if post:
            cfg = self.leggi_cfg()

            estrai = Estrai()

            for doc in cfg:
                setattr(estrai, doc, cfg[doc])

            # esegue l'estrazione dei documenti
            # estrazione_da_excel(estrai=estrai)

        return {'struttura': preferenze['documenti'],
                'estrazione': preferenze['estrazione'],
                'filtro_impresa': preferenze['filtro_impresa'],
                'filtro_cantiere': preferenze['filtro_cantiere'],
                }

    def aggiorna_lista_cantieri(self):
        cantieri = Cantiere.objects.all()

        for cantiere in cantieri:

            if not self.parser.has_option('filtro_cantiere', cantiere.nome):
                self.parser.set('filtro_cantiere', cantiere.nome, '0')

        with open('estrai_dati.txt', 'w') as configfile:
            self.parser.write(configfile)
