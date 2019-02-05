import datetime
import glob
import os
import shutil

import pandas as pd
from django.http import HttpResponse

from personale.models import Azienda, Lavoratore, Cantiere

FIN = '190129 AC Boiler.xlsx'

PATH_HOME = os.getcwd()
PATH = r'C:\Users\leonardo.masi\Documents\Personale'
PATH2 = r'C:\Users\leonardo.masi\Documents\Programmi\Richiesta_Dati'


class Estrai:
    def __init__(self):
        # base
        self.unilav = 1
        self.idoneita = 1

        # formazione
        self.art37 = 1
        self.preposto = 1
        self.primo_soccorso = 1
        self.antincendio = 1
        self.h2s = 1
        self.dpi3 = 1
        self.muletto = 1
        self.ple = 1
        self.gru = 1
        self.imbracatore = 1
        self.spazi_confinati = 1
        self.ponteggi = 1
        self.rir = 1

        # nomine
        self.nomina_preposto = 1
        self.nomina_primo_soccorso = 1
        self.nomina_antincendio = 1

    def formazione(self):
        attestati = ('art37' * self.art37, 'preposto' * self.preposto, 'primo.soccorso' * self.primo_soccorso,
                     'antincendio' * self.antincendio, 'h2s' * self.h2s, 'dpi3' * self.dpi3, 'carrelli' * self.muletto,
                     'ple' * self.ple, 'autogru' * self.gru, 'imbracatore' * self.imbracatore,
                     'spazi.confinati' * self.spazi_confinati, 'ponteggi' * self.ponteggi, 'rir' * self.rir)
        return attestati

    def formazione_tutti(self):
        self.art37 = self.preposto = self.primo_soccorso = self.antincendio = self.h2s = self.dpi3 = self.muletto = 1
        self.ple = self.gru = self.imbracatore = self.spazi_confinati = self.ponteggi = self.rir = 1
        return self.formazione()

    def nomine(self):
        incarico = ('nomina.preposto' * self.nomina_preposto, 'nomina.primo.soccorso' * self.nomina_primo_soccorso,
                    'nomina.antincendio' * self.nomina_antincendio)
        return incarico

    def nomine_tutte(self):
        self.nomina_preposto = self.nomina_primo_soccorso = self.nomina_antincendio = 1
        return self.nomine()

    def estrai(self, cognome, nome):
        pass


def copia(path_da, nome_pdf, cognome, nome, nome_documento):
    da = os.path.join(path_da, nome_pdf)
    a = os.path.join(PATH2, '%s %s - %s.pdf' % (cognome, nome, nome_documento))
    # print(da, '-->', a)
    print('  ', nome_documento)
    shutil.copy(da, a)


def estrai_dati_da_excel():
    xls = pd.ExcelFile(os.path.join(PATH2, FIN))
    df = xls.parse('1d')
    estrai = Estrai()

    for row in df.iterrows():
        cognome = row[1]['Cognome']
        nome = row[1]['Nome']
        print(cognome, nome)

        path_lavoratore = os.path.join(PATH, "%s %s" % (cognome, nome))
        path_attestati = os.path.join(PATH, "%s %s" % (cognome, nome), 'attestati')
        path_nomine = os.path.join(PATH, "%s %s" % (cognome, nome), 'nomine')

        # documenti base
        os.chdir(path_lavoratore)

        if estrai.unilav:
            unilav = glob.glob('unilav*.pdf')

            if unilav:
                copia(path_lavoratore, unilav[0], cognome, nome, 'unilav')

        if estrai.idoneita:
            idoneita = glob.glob('idoneit*.pdf')

            if idoneita:
                copia(path_lavoratore, idoneita[0], cognome, nome, 'idoneità')

        # attestati corsi formazione
        if os.path.isdir(path_attestati):
            os.chdir(path_attestati)

            for corso in estrai.formazione():
                certificato = glob.glob('%s*.pdf' % corso)
                if certificato:
                    copia(path_attestati, certificato[0], cognome, nome, corso)

        # lettere incarico
        if os.path.isdir(path_nomine):
            os.chdir(path_nomine)

            for nomina in estrai.nomine():
                incarico = glob.glob('%s*.pdf' % nomina)

                if incarico:
                    copia(path_nomine, incarico[0], cognome, nome, nomina)

    os.chdir(PATH_HOME)


def estrai_cantiere(azienda=None, cantiere=None):
    estrai = Estrai()

    if azienda:
        azienda = Azienda.objects.get(nome=azienda)

    if cantiere:
        cantiere = Cantiere.objects.get(nome=cantiere)
        print(cantiere)

    lavoratori = Lavoratore.objects.filter(cantiere=cantiere)

    for lavoratore in lavoratori:
        cognome = lavoratore.cognome
        nome = lavoratore.nome
        print(cognome, nome)

        path_lavoratore = os.path.join(PATH, "%s %s" % (cognome, nome))
        path_attestati = os.path.join(PATH, "%s %s" % (cognome, nome), 'attestati')
        path_nomine = os.path.join(PATH, "%s %s" % (cognome, nome), 'nomine')

        # documenti base
        os.chdir(path_lavoratore)

        if estrai.unilav:
            unilav = glob.glob('unilav*.pdf')

            if unilav:
                copia(path_lavoratore, unilav[0], cognome, nome, 'unilav')

        if estrai.idoneita:
            idoneita = glob.glob('idoneit*.pdf')

            if idoneita:
                copia(path_lavoratore, idoneita[0], cognome, nome, 'idoneità')

        # attestati corsi formazione
        if os.path.isdir(path_attestati):
            os.chdir(path_attestati)

            for corso in estrai.formazione():
                certificato = glob.glob('%s*.pdf' % corso)
                if certificato:
                    copia(path_attestati, certificato[0], cognome, nome, corso)

        # lettere incarico
        if os.path.isdir(path_nomine):
            os.chdir(path_nomine)

            for nomina in estrai.nomine():
                incarico = glob.glob('%s*.pdf' % nomina)

                if incarico:
                    copia(path_nomine, incarico[0], cognome, nome, nomina)

    os.chdir(PATH_HOME)


def estrai_dati(request):
    estrai_cantiere(cantiere='Andritz')
