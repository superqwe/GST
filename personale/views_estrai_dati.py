import glob
import os
import shutil

from pprint import pprint as pp

import pandas as pd
from django.db.models import Q

from personale.models import Azienda, Lavoratore, Cantiere

# FILE_XLS = '190410 Personale x FINCOSIT.xlsx'
# # FILE_XLS = '190417 Macchi.xlsx'
# NOME_FOGLIO = 'Foglio1'

FILE_XLS = '190513 Tenova.xlsx'
NOME_FOGLIO = 'Foglio1'

PATH_HOME = os.getcwd()
PATH = r'C:\Users\leonardo.masi\Documents\Personale'
PATH2 = r'C:\Users\leonardo.masi\Documents\Programmi\Richiesta_Dati'

ESTRAI_TUTTO = False


def indice_data_piu_recente_ggmmaa(elenco_date):
    """restituisce l'indice dell'elenco documenti contenente la data più recente"""
    elenco_date = [x.split()[-1].split('.')[0] for x in elenco_date]
    elenco_date = [('%s%s%s' % (x[-2:], x[2:-2], x[:2]), i) for i, x in enumerate(elenco_date)]
    elenco_date.sort(reverse=True)

    return (elenco_date[0][1])

#todo: ponteggi viene sempre estratto
#todo: apvr non viene estratto
class Estrai(object):
    def __init__(self):
        # base/vari
        self.unilav = 0
        self.idoneita = 0
        self.ci = 0
        self.codice_fiscale = 0
        self.foto = 0
        self.consegna_dpi = 0

        # formazione
        self.art37 = 0
        self.preposto = 0
        self.primo_soccorso = 0
        self.antincendio = 0
        self.h2s = 0
        self.dpi3 = 0
        self.apvr = 0
        self.lavori_quota = 0
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
        self.nomina_antincendio = 0

    def formazione(self):
        attestati = filter(lambda x: x != '',
                           ('art37' * self.art37, 'preposto' * self.preposto, 'primo.soccorso' * self.primo_soccorso,
                            'antincendio' * self.antincendio, 'h2s' * self.h2s, 'dpi3' * self.dpi3, 'avpr' * self.apvr,
                            'lavori.quota' * self.lavori_quota, 'carrelli' * self.muletto, 'ple' * self.ple,
                            'autogru' * self.gru, 'imbracatore' * self.imbracatore,
                            'spazi.confinati' * self.spazi_confinati, 'ponteggi' * self.ponteggi, 'rir' * self.rir,
                            'rls' * self.rls)
                           )
        return attestati

    def formazione_tutti(self, scelta=True):
        self.art37 = self.preposto = self.primo_soccorso = self.antincendio = self.h2s = self.dpi3 = self.apvr = scelta
        self.lavori_quota = self.muletto = self.ple = self.gru = self.imbracatore = self.spazi_confinati = scelta
        self.ponteggi = self.rir == scelta
        return self.formazione()

    def nomine(self):
        incarico = filter(lambda x: x != '',
                          ('nomina.preposto' * self.nomina_preposto,
                           'nomina.primo.soccorso' * self.nomina_primo_soccorso,
                           'nomina.antincendio' * self.nomina_antincendio))
        return incarico

    def nomine_tutte(self, scelta=True):
        self.nomina_preposto = self.nomina_primo_soccorso = self.nomina_antincendio = scelta
        return self.nomine()

    def resetta(self):
        self.unilav = False
        self.idoneita = False
        self.consegna_dpi = False
        self.formazione_tutti(False)
        self.nomine_tutte(False)

    def estrai(self, cognome, nome, documenti=None):

        if pd.isna(cognome):
            return

        for doc in documenti:
            setattr(self, doc, 1)

        cognome = cognome.strip().replace(' ', '_')
        nome = nome.strip()
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

        if self.consegna_dpi:
            consegna_dpi = glob.glob('dpi\consegna.dpi*.pdf')

            if consegna_dpi:
                indice = 0

                if len(consegna_dpi) > 1:
                    indice = indice_data_piu_recente_ggmmaa(consegna_dpi)

                copia(path_lavoratore, consegna_dpi[indice], cognome, nome, 'consegna_dpi')

        if self.ci:
            ci = glob.glob('doc*.pdf')

            if ci:
                copia(path_lavoratore, ci[0], cognome, nome, 'doc')

        if self.codice_fiscale:
            codice_fiscale = glob.glob('cf*.pdf')

            if codice_fiscale:
                copia(path_lavoratore, codice_fiscale[0], cognome, nome, 'cf')

        if self.foto:
            foto = glob.glob('foto*.*')

            if foto:
                copia(path_lavoratore, foto[0], cognome, nome, 'foto')

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

    if nome_documento != 'foto':
        a = os.path.join(PATH2, '%s %s - %s.pdf' % (cognome, nome, nome_documento))
    else:
        a = os.path.join(PATH2, '%s %s - %s.jpg' % (cognome, nome, nome_documento))

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


def estrazione_selettiva2(aziende=None, cantieri=None, documenti=None):
    estrai = Estrai()
    estrai.resetta()

    lavoratori = Lavoratore.objects.filter(in_forza=True)

    if aziende:
        aziende = [azienda.title() for azienda in aziende]

        lavoratori = lavoratori.filter(azienda__nome__in=aziende)

    if cantieri:
        filtro_cantieri = Q()

        for cantiere in cantieri:
            filtro_cantieri |= Q(nome__iexact=cantiere)
        cantieri = Cantiere.objects.filter(filtro_cantieri)

        lavoratori = lavoratori.filter(cantiere__in=cantieri)

    for lavoratore in lavoratori:
        cognome = lavoratore.cognome
        nome = lavoratore.nome

        estrai.estrai(cognome, nome, documenti)

    os.chdir(PATH_HOME)

    return lavoratori


def estrazione_da_excel2(fin=None, documenti=None):
    fin = fin

    try:
        xls = pd.ExcelFile(os.path.join(PATH2, fin))
    except FileNotFoundError:
        return 'Il File "%s" non esiste' % fin

    df = xls.parse(NOME_FOGLIO)

    estrai = Estrai()
    estrai.resetta()

    lavoratori = []
    for row in df.iterrows():
        cognome = row[1]['Cognome']
        nome = row[1]['Nome']
        # print(cognome, nome)

        if not pd.isna(cognome):
            try:
                lavoratore = Lavoratore.objects.get(cognome=cognome.strip().title(), nome=nome.strip().title())
                estrai.estrai(cognome, nome, documenti)
            except Lavoratore.DoesNotExist:
                lavoratore = {'cognome': cognome, 'nome': nome, 'non_esiste': True}

            lavoratori.append(lavoratore)

    os.chdir(PATH_HOME)
    return lavoratori
