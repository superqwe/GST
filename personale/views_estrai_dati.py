import glob
import os
import shutil
from configparser import ConfigParser

import pandas as pd

from personale.models import Azienda, Lavoratore, Cantiere

from pprint import pprint as pp

# FILE_XLS = '190410 Personale x FINCOSIT.xlsx'
# # FILE_XLS = '190417 Macchi.xlsx'
# NOME_FOGLIO = 'Foglio1'

FILE_XLS = '190513 Tenova.xlsx'
NOME_FOGLIO = 'Foglio1'

PATH_HOME = os.getcwd()
PATH = r'C:\Users\leonardo.masi\Documents\Personale'
PATH2 = r'C:\Users\leonardo.masi\Documents\Programmi\Richiesta_Dati'

ESTRAI_TUTTO = False


class Estrai(object):
    def __init__(self):
        # base
        self.unilav = 0
        self.idoneita = 0

        # formazione
        self.art37 = 0
        self.preposto = 0
        self.primo_soccorso = 0
        self.antincendio = 0
        self.h2s = 0
        self.dpi3 = 0
        self.muletto = 0
        self.ple = 0
        self.gru = 0
        self.imbracatore = 0
        self.spazi_confinati = 0
        self.ponteggi = 0
        self.rir = 0
        self.rls = 0

        # nomine
        self.nomina_preposto = 0
        self.nomina_primo_soccorso = 0
        self.nomina_antincendio = 1

    def formazione(self):
        attestati = filter(lambda x: x != '',
                           ('art37' * self.art37, 'preposto' * self.preposto, 'primo.soccorso' * self.primo_soccorso,
                            'antincendio' * self.antincendio, 'h2s' * self.h2s, 'dpi3' * self.dpi3,
                            'carrelli' * self.muletto, 'ple' * self.ple, 'autogru' * self.gru,
                            'imbracatore' * self.imbracatore, 'spazi.confinati' * self.spazi_confinati,
                            'ponteggi' * self.ponteggi, 'rir' * self.rir, 'rls' * self.rls)
                           )
        return attestati

    def formazione_tutti(self):
        self.art37 = self.preposto = self.primo_soccorso = self.antincendio = self.h2s = self.dpi3 = self.muletto = 1
        self.ple = self.gru = self.imbracatore = self.spazi_confinati = self.ponteggi = self.rir = 1
        return self.formazione()

    def nomine(self):
        incarico = filter(lambda x: x != '',
                          ('nomina.preposto' * self.nomina_preposto,
                           'nomina.primo.soccorso' * self.nomina_primo_soccorso,
                           'nomina.antincendio' * self.nomina_antincendio))
        return incarico

    def nomine_tutte(self):
        self.nomina_preposto = self.nomina_primo_soccorso = self.nomina_antincendio = 1
        return self.nomine()

    def estrai(self, cognome, nome):

        if pd.isna(cognome):
            return

        cognome = cognome.strip().replace(' ', '_')
        print(cognome, nome)

        path_lavoratore = os.path.join(PATH, "%s %s" % (cognome, nome))
        path_attestati = os.path.join(PATH, "%s %s" % (cognome, nome), 'attestati')
        path_nomine = os.path.join(PATH, "%s %s" % (cognome, nome), 'nomine')

        # documenti base
        try:
            os.chdir(path_lavoratore)
        except FileNotFoundError:
            print('   ----------> Non esiste')
            return

        if self.unilav:
            unilav = glob.glob('unilav*.pdf')

            if unilav:
                copia(path_lavoratore, unilav[0], cognome, nome, 'unilav')

        if self.idoneita:
            idoneita = glob.glob('idoneit*.pdf')

            if idoneita:
                copia(path_lavoratore, idoneita[0], cognome, nome, 'idoneità')

        # attestati corsi formazione
        if os.path.isdir(path_attestati):
            os.chdir(path_attestati)

            for corso in self.formazione():
                certificato = glob.glob('%s*.pdf' % corso)
                if certificato:
                    copia(path_attestati, certificato[0], cognome, nome, corso)

        # lettere incarico
        if os.path.isdir(path_nomine):
            os.chdir(path_nomine)

            for nomina in self.nomine():
                incarico = glob.glob('%s*.pdf' % nomina)

                if incarico:
                    copia(path_nomine, incarico[0], cognome, nome, nomina)


def copia(path_da, nome_pdf, cognome, nome, nome_documento):
    da = os.path.join(path_da, nome_pdf)
    a = os.path.join(PATH2, '%s %s - %s.pdf' % (cognome, nome, nome_documento))
    # print(da, '-->', a)
    print('  ', nome_documento)
    shutil.copy(da, a)


def estrazione_da_excel(tutto=False, estrai=None):
    fin = FILE_XLS

    try:
        xls = pd.ExcelFile(os.path.join(PATH2, fin))
    except FileNotFoundError:
        return 'Il File "%s" non esiste' % fin

    df = xls.parse(NOME_FOGLIO)

    if not estrai:
        estrai = Estrai()

    if tutto:
        estrai.formazione_tutti()

    for row in df.iterrows():
        cognome = row[1]['Cognome']
        nome = row[1]['Nome']

        estrai.estrai(cognome, nome)

    os.chdir(PATH_HOME)


def estrazione_selettiva(azienda=None, cantiere=None):
    estrai = Estrai()

    lavoratori = Lavoratore.objects.all()

    if azienda:
        lavoratori = lavoratori.filter(azienda=Azienda.objects.get(nome=azienda))

    if cantiere:
        lavoratori = lavoratori.filter(cantiere=Cantiere.objects.get(nome=cantiere))

    for lavoratore in lavoratori:
        cognome = lavoratore.cognome
        nome = lavoratore.nome

        estrai.estrai(cognome, nome)

    os.chdir(PATH_HOME)

    return


def estrai_principale(request):
    errore = estrazione_selettiva(azienda='Modomec')
    # estrazione_selettiva(cantiere='Massafra', azienda='Modomec')
    # errore = estrazione_da_excel(ESTRAI_TUTTO)
    return errore


def leggi_cfg():
    parser = ConfigParser()
    parser.read('estrai_dati.txt')

    elenco_attestati = {}

    # todo: da implementare la selezion multipla per categoria documento
    tutto, base, formazione, nomine = parser.items('tutto')

    for sec in parser.sections():

        for k, v in parser.items(sec):
            elenco_attestati[k] = 0 if v == '0' else 1

    return elenco_attestati


def leggi_cfg2():
    parser = ConfigParser()
    parser.read('estrai_dati.txt')

    # estrazione = ((k, v) for k, v in parser.items('estrazione'))
    estrazione = {'tipo_estrazione': parser.get('estrazione', 'tipo')}
    base = ((k, True if v == '1' else False) for k, v in parser.items('base'))
    formazione = ((k, True if v == '1' else False) for k, v in parser.items('formazione'))
    nomine = ((k, True if v == '1' else False) for k, v in parser.items('nomine'))

    struttura = {'estrazione': estrazione,
                 'documenti': (('Base', base), ('Formazione', formazione), ('Nomine', nomine))}

    return struttura


def scrivi_cfg(dati):
    # pp(dati)
    parser = ConfigParser()
    parser.read('estrai_dati.txt')

    for sec in parser.sections():

        for k in parser.items(sec):
            parser.set(sec, k[0], '0')

    for k in dati:

        for sec in parser.sections():

            if parser.has_option(sec, k):
                parser.set(sec, k, '1')

    parser.set('estrazione', 'tipo', dati['tipo_estrazione'])

    with open('estrai_dati.txt', 'w') as configfile:
        parser.write(configfile)


def estrai_cfg(post):
    preferenze = leggi_cfg2()

    if post:
        cfg = leggi_cfg()
        del cfg['formazione']
        del cfg['tutto']
        del cfg['base']
        del cfg['nomine']
        # del cfg['estrazione']

        estrai = Estrai()

        for doc in cfg:
            setattr(estrai, doc, cfg[doc])

        # estrazione_da_excel(estrai=estrai)

    return {'struttura': preferenze['documenti'],
            'estrazione': preferenze['estrazione']}
