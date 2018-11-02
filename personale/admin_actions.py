import datetime
import os
import re
from pprint import pprint as pp

import pandas as pd
from django.contrib import admin

from personale.models import Anagrafica, Formazione, Lavoratore

OGGI = datetime.date.today()
DT = datetime.timedelta(30)
AVVISO_SCADENZA = OGGI + DT
PATH_BASE = "C:\\Users\\leonardo.masi\\Documents\\Personale"


def scadenza2date(documento, durata=5):
    re_dma = re.compile(r'\d{2}\.\d{2}\.\d{2,4}')

    if not re_dma.findall(documento):
        re_dma = re.compile(r'\d{6,8}')

        try:
            data = re_dma.findall(documento)[0]

            giorno, mese, anno = int(data[:2]), int(data[2:4]), int(data[4:])
            anno = anno if anno > 2000 else anno + 2000
            scadenza = datetime.date(anno + durata, mese, giorno)
            return scadenza
        except IndexError:
            print('+++', documento)
            return None

    try:
        giorno, mese, anno = re_dma.findall(documento)[0].split('.')
        anno = int(anno) if len(anno) == 4 else int(anno) + 2000
        scadenza = datetime.date(anno + durata, int(mese), int(giorno))
        return scadenza
    except IndexError:
        print('+++', documento)
        return None


def aggiorna_lavoratori():
    # aggiorna elenco lavoratori
    path_base = PATH_BASE

    print('*' * 450)

    primo_ciclo = True
    for root, dirs, files in os.walk(path_base):

        for lavoratore in dirs:
            lavoratore = lavoratore.strip().title().split(maxsplit=1)

            if lavoratore[0] != 'Z':
                if primo_ciclo:

                    cognome, nome = lavoratore

                    try:
                        res = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]
                    except IndexError:
                        lavoratore = Lavoratore(cognome=cognome, nome=nome)
                        lavoratore.save()
                        print('Nuovo Lavoratore: ', lavoratore)

        primo_ciclo = False

    # crea la formazione per ogni lavoratore
    lavoratori = Lavoratore.objects.all()

    for lavoratore in lavoratori:
        res = Formazione.objects.filter(lavoratore__id=lavoratore.id)

        # break

        if len(res) == 0:
            formazione = Formazione(lavoratore=lavoratore)
            formazione.save()
            print('Nuova Formazione: ', lavoratore)


def aggiorna_attestati():
    path_base = PATH_BASE

    for root, dirs, files in os.walk(path_base):
        path = root[len(path_base) + 1:].lower()

        if not path.startswith('z ') and not 'scaduti' in root:
            try:
                cognome, nome = path.title().split('\\')[0].split(maxsplit=1)
                print('\n', cognome, nome)
                lavoratore = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]
                formazione = Formazione.objects.get(lavoratore__id=lavoratore.id)

                for documento in files:
                    documento = documento.lower()

                    if documento.endswith('.pdf'):
                        tipo, scadenza = documento.split()[:2]

                        if tipo == 'doc':
                            scadenza = scadenza2date(documento, 0)
                            formazione.ci = scadenza

                        elif tipo in ('idoneità', 'idoneita'):
                            scadenza = scadenza2date(documento, 0)
                            formazione.idoneita = scadenza

                        elif tipo == 'unilav':
                            scadenza = scadenza2date(documento, 0)
                            formazione.unilav = scadenza

                        elif tipo in ('art37', 'art.37'):
                            scadenza = scadenza2date(documento)
                            formazione.art37 = scadenza

                        elif tipo in ('primo', 'primosoccorso', 'primo.soccorso'):
                            scadenza = scadenza2date(documento, 3)
                            formazione.primo_soccorso = scadenza

                        elif tipo == 'antincendio':
                            scadenza = scadenza2date(documento, 0)
                            formazione.antincendio = scadenza

                        elif tipo == 'preposto':
                            scadenza = scadenza2date(documento)
                            formazione.preposto = scadenza

                        elif tipo in ('h2s.safety', 'h2s'):
                            scadenza = scadenza2date(documento)
                            formazione.h2s = scadenza

                        elif tipo == 'dpi':
                            scadenza = scadenza2date(documento)
                            formazione.dpi3 = scadenza

                        elif tipo in ('carrelli', 'carrello', 'sollevatore'):
                            scadenza = scadenza2date(documento)
                            formazione.carrello = scadenza

                        elif tipo == 'ple':
                            scadenza = scadenza2date(documento)
                            formazione.ple = scadenza

                        elif tipo in ('autogru', 'gru'):
                            scadenza = scadenza2date(documento)
                            formazione.gru = scadenza

                        elif tipo == 'imbracatore':
                            scadenza = scadenza2date(documento)
                            formazione.imbracatore = scadenza

                        elif tipo in ('spazi', 'spazio', 'spazio.confinato', 'spazi.confinati'):
                            scadenza = scadenza2date(documento)
                            formazione.spazi_confinati = scadenza

                        elif tipo in ('altro', 'rir'):
                            scadenza = scadenza2date(documento)
                            formazione.rir = scadenza

                        elif tipo == 'rls':
                            scadenza = scadenza2date(documento, 1)
                            formazione.rls = scadenza

                        elif tipo == 'rspp':
                            scadenza = scadenza2date(documento)
                            formazione.rspp = scadenza

                        elif tipo == 'ponteggi':
                            scadenza = scadenza2date(documento, 4)
                            formazione.ponteggi = scadenza

                        else:
                            print('***', tipo, '+++', documento)

                formazione.save()

            except ValueError:
                print('*** Errore in ', path)


def m_d_y2mdy(scadenza):
    re_dma = re.compile(r'\d{2}\.\d{2}\.\d{2,4}')

    if not re_dma.findall(scadenza):
        re_dma = re.compile(r'\d{6,8}')

        try:
            data = re_dma.findall(scadenza)[0]

            giorno, mese, anno = int(data[:2]), int(data[2:4]), int(data[4:])
            anno = anno - 2000 if anno > 2000 else anno
            scadenza = '%2i%i2%2i' % (giorno, mese, anno)
            return scadenza
        except IndexError:
            print('+++', scadenza)
            return None

    try:
        giorno, mese, anno = re_dma.findall(scadenza)[0].split('.')
        anno = int(anno) - 2000 if len(anno) == 4 else int(anno)
        scadenza = '%s%s%2i' % (giorno, mese, anno)
        return scadenza
    except IndexError:
        print('+++', scadenza)
        return None


def rinomina_attestati():
    path_base = PATH_BASE
    print('*'*400)

    for root, dirs, files in os.walk(path_base):
        path = root[len(path_base) + 1:].lower()

        if not path.startswith('z ') and not 'scaduti' in root:
            try:
                cognome, nome = path.title().split('\\')[0].split(maxsplit=1)
                print('\n', cognome, nome)
                lavoratore = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]
                formazione = Formazione.objects.get(lavoratore__id=lavoratore.id)

                for documento in files:
                    documento = documento.lower()

                    if documento.endswith('.pdf'):
                        tipo, data = documento.split()[:2]

                        if tipo == 'doc':
                            scadenza = m_d_y2mdy(data)
                            tipo = 'doc'

                        elif tipo in ('idoneità', 'idoneita'):
                            scadenza = m_d_y2mdy(data)
                            tipo = 'idoneità'

                        elif tipo == 'unilav':
                            scadenza = m_d_y2mdy(data)
                            tipo = 'unilav'

                        elif tipo in ('art37', 'art.37'):
                            scadenza = m_d_y2mdy(data)
                            tipo = 'art37'

                        elif tipo in ('primo', 'primosoccorso', 'primo.soccorso'):
                            scadenza = m_d_y2mdy(data)
                            tipo = 'primo.soccorso'

                        elif tipo == 'antincendio':
                            scadenza = m_d_y2mdy(data)
                            tipo = 'antincendio'

                        elif tipo == 'preposto':
                            scadenza = m_d_y2mdy(data)
                            tipo = 'preposto'

                        elif tipo in ('h2s.safety', 'h2s'):
                            scadenza = m_d_y2mdy(data)
                            tipo = 'h2s'

                        elif tipo == 'dpi':
                            scadenza = m_d_y2mdy(data)
                            tipo = 'dpi'

                        elif tipo in ('carrelli', 'carrello', 'sollevatore'):
                            scadenza = m_d_y2mdy(data)
                            tipo = 'carrelli'

                        elif tipo == 'ple':
                            scadenza = m_d_y2mdy(data)
                            tipo = 'ple'

                        elif tipo in ('autogru', 'gru'):
                            scadenza = m_d_y2mdy(data)
                            tipo = 'autogru'

                        elif tipo == 'imbracatore':
                            scadenza = m_d_y2mdy(data)
                            tipo = 'imbracatore'

                        elif tipo in ('spazi', 'spazio', 'spazio.confinato'):
                            scadenza = m_d_y2mdy(data)
                            tipo = 'spazi.confinati'

                        elif tipo in ('altro', 'rir'):
                            scadenza = m_d_y2mdy(data)
                            tipo = 'rir'

                        elif tipo == 'rls':
                            scadenza = m_d_y2mdy(data)
                            tipo = 'rls'

                        elif tipo == 'rspp':
                            scadenza = m_d_y2mdy(data)
                            tipo = 'rspp'

                        elif tipo == 'ponteggi':
                            scadenza = m_d_y2mdy(data)
                            tipo = 'ponteggi'

                        else:
                            print('***', tipo, '+++', documento)

                    print(tipo, scadenza)


            except ValueError:
                print('*** Errore in ', path)
