import datetime
import glob
import os
import shutil

import pandas as pd
from django.http import HttpResponse

FIN = '190129 AC Boiler.xlsx'

PATH_HOME = os.getcwd()
PATH = r'C:\Users\leonardo.masi\Documents\Personale'
PATH2 = r'C:\Users\leonardo.masi\Documents\Programmi\Richiesta_Dati'


class Estrai:
    unilav = 1
    idoneita = 1

    # formazione
    art37 = 1
    preposto = 1
    primo_soccorso = 1
    antincendio = 1
    h2s = 1
    dpi3 = 1
    muletto = 1
    ple = 1
    gru = 1
    imbracatore = 1
    spazi_confinati = 1
    ponteggi = 1
    rir = 1

    # nomine
    nomina_preposto = 1
    nomina_primo_soccorso = 1
    nomina_antincendio = 1

    def formazione(self):
        attestati = ('art37' * self.art37, 'preposto' * self.preposto, 'primo.soccorso' * self.primo_soccorso,
                     'antincendio' * self.antincendio, 'h2s' * self.h2s, 'dpi3' * self.dpi3,
                     'carrelli' * self.muletto, 'ple' * self.ple, 'autogru' * self.gru,
                     'imbracatore' * self.imbracatore, 'spazi.confinati' * self.spazi_confinati,
                     'ponteggi' * self.ponteggi, 'rir' * self.rir)
        return attestati

    def nomine(self):
        incarico = ('nomina.preposto' * self.nomina_preposto, 'nomina.primo.soccorso' * self.nomina_primo_soccorso,
                    'nomina.antincendio' * self.nomina_antincendio)
        return incarico


def copia(path_da, nome_pdf, cognome, nome, nome_documento):
    da = os.path.join(path_da, nome_pdf)
    a = os.path.join(PATH2, '%s %s - %s.pdf' % (cognome, nome, nome_documento))
    # print(da, '-->', a)
    print('  ', nome_documento)
    shutil.copy(da, a)


def estrai_dati2(request):
    xls = pd.ExcelFile(os.path.join(PATH2, FIN))
    df = xls.parse('1d')

    for row in df.iterrows():
        cognome = row[1]['Cognome']
        nome = row[1]['Nome']
        # lavoratore = Lavoratore.objects.get(cognome=cognome, nome=nome)

        print(cognome, nome)

        path_lavoratore = os.path.join(PATH, "%s %s" % (cognome, nome))
        path_attestati = os.path.join(PATH, "%s %s" % (cognome, nome), 'attestati')
        path_nomine = os.path.join(PATH, "%s %s" % (cognome, nome), 'nomine')

        # documenti base
        os.chdir(path_lavoratore)

        if Estrai.unilav:
            unilav = glob.glob('unilav*.pdf')

            if unilav:
                copia(path_lavoratore, unilav[0], cognome, nome, 'unilav')

        if Estrai.idoneita:
            idoneita = glob.glob('idoneit*.pdf')

            if idoneita:
                copia(path_lavoratore, idoneita[0], cognome, nome, 'idoneità')

        # attestati corsi formazione
        if os.path.isdir(path_attestati):
            os.chdir(path_attestati)

            for corso in Estrai.formazione(Estrai):
                certificato = glob.glob('%s*.pdf' % corso)
                if certificato:
                    copia(path_attestati, certificato[0], cognome, nome, corso)

        # lettere incarico
        if os.path.isdir(path_nomine):
            os.chdir(path_nomine)

            for nomina in Estrai.nomine(Estrai):
                incarico = glob.glob('%s*.pdf' % nomina)

                if incarico:
                    copia(path_nomine, incarico[0], cognome, nome, nomina)

    os.chdir(PATH_HOME)
