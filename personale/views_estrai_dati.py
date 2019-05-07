import glob
import os
import shutil

import pandas as pd

from personale.models import Azienda, Lavoratore, Cantiere

# FILE_XLS = '190410 Personale x FINCOSIT.xlsx'
# # FILE_XLS = '190417 Macchi.xlsx'
# NOME_FOGLIO = 'Foglio1'

FILE_XLS = '190502 Tenova.xlsx'
NOME_FOGLIO = 'Foglio1'

PATH_HOME = os.getcwd()
PATH = r'C:\Users\leonardo.masi\Documents\Personale'
PATH2 = r'C:\Users\leonardo.masi\Documents\Programmi\Richiesta_Dati'


class Estrai:
    def __init__(self):
        # base
        self.unilav = 1
        self.idoneita = 1

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
        self.nomina_antincendio = 0

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


def estrazione_da_excel(tutto=False):
    fin = FILE_XLS

    try:
        xls = pd.ExcelFile(os.path.join(PATH2, fin))
    except FileNotFoundError:
        return 'Il File "%s" non esiste' % fin

    df = xls.parse(NOME_FOGLIO)
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


def estrai_principale(request):
    # estrazione_selettiva(azienda='Modomec')
    # estrazione_selettiva(cantiere='Massafra', azienda='Modomec')
    errore = estrazione_da_excel(True)
    return errore
