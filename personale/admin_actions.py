import datetime
import os
import re
import time
from pprint import pprint as pp

import pandas as pd

from personale import admin_actions_anagrafica, admin_actions_formazione
from personale.models import Anagrafica, Formazione, Lavoratore, Nomine

ADESSO = time.time()
OGGI = datetime.date.today()
DT = datetime.timedelta(30)
DT_6_MESI = datetime.timedelta(30 * 6)
AVVISO_SCADENZA = OGGI + DT
AVVISO_SCADENZA_ATTESTATI = OGGI + DT_6_MESI
PATH_BASE = "C:\\Users\\leonardo.masi\\Documents\\Personale"

FILE_DATA_ULTIMA_MODIFICA = 'data ultima modifica.txt'


def m_d_y2mdy(scadenza, tipo=None):
    if tipo:
        print('+' * 30, scadenza)

    re_dma = re.compile(r'\d{2}\.\d{2}\.\d{2,4}')

    if not re_dma.findall(scadenza):
        re_dma = re.compile(r'\d{6,8}')

        try:
            data = re_dma.findall(scadenza)[0]

            giorno, mese, anno = int(data[:2]), int(data[2:4]), int(data[4:])
            anno = anno - 2000 if anno > 2000 else anno
            scadenza = '%02i%02i%02i' % (giorno, mese, anno)
            return scadenza
        except IndexError:
            print('+++', scadenza)
            return None

    try:
        giorno, mese, anno = re_dma.findall(scadenza)[0].split('.')
        anno = int(anno) - 2000 if len(anno) == 4 else int(anno)
        scadenza = '%s%s%02i' % (giorno, mese, anno)
        return scadenza
    except IndexError:
        print('+++', scadenza)
        return None


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


def aggiorna_stato_lavoratori():
    #todo da aggiornare
    admin_actions_anagrafica.aggiorna_stato_anagrafica()
    admin_actions_formazione.aggiorna_stato_formazione()


def rinomina_attestati():
    #todo obsoleto da aggiornare
    path_base = PATH_BASE
    print('*' * 400)

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
                        scadenza = None

                        if tipo == 'doc':
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'doc'

                        elif tipo in ('idoneità', 'idoneita'):
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'idoneità'

                        elif tipo == 'unilav':
                            if data.split('.')[0] == 'indeterminato':
                                scadenza = 'indeterminato'
                            else:
                                scadenza = m_d_y2mdy(documento)

                            tipo = 'unilav'

                        elif tipo in ('art37', 'art.37'):
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'art37'

                        elif tipo in ('primo', 'primosoccorso', 'primo.soccorso'):
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'primo.soccorso'

                        elif tipo == 'antincendio':
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'antincendio'

                        elif tipo == 'preposto':
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'preposto'

                        elif tipo in ('h2s.safety', 'h2s'):
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'h2s'

                        elif tipo == 'dpi':
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'dpi'

                        elif tipo in ('carrelli', 'carrello', 'sollevatore'):
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'carrelli'

                        elif tipo == 'ple':
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'ple'

                        elif tipo in ('autogru', 'gru'):
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'autogru'

                        elif tipo == 'imbracatore':
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'imbracatore'

                        elif tipo in ('spazi', 'spazio', 'spazio.confinato', 'spazi.confinato', 'spazi.confinati'):
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'spazi.confinati'

                        elif tipo in ('altro', 'rir'):
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'rir'

                        elif tipo == 'rls':
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'rls'

                        elif tipo == 'rspp':
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'rspp'

                        elif tipo == 'ponteggi':
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'ponteggi'

                        elif tipo == 'lavori.quota':
                            scadenza = m_d_y2mdy(documento)
                            tipo = 'lavori.quota'

                        else:
                            print('***', tipo, '+++', documento)

                    # a cosa serve???
                    # if scadenza:
                    #     da = os.path.join(PATH_BASE, path, documento)
                    #     a = os.path.join(PATH_BASE, path, '%s %s.pdf' % (tipo, scadenza))
                    #     os.rename(da, a)
                    # else:
                    #     print(cognome, nome)

            except ValueError:
                print('*** Errore in ', path)


def aggiorna_scadenza_documenti():
    path_base = PATH_BASE

    lavoratori = Anagrafica.objects.filter(in_forza=True).values_list('lavoratore__cognome', 'lavoratore__nome')

    for root, dirs, files in os.walk(path_base):
        path = root[len(path_base) + 1:].lower()

        if not path.startswith('z ') and not 'scaduti' in root:
            try:
                cognome, nome = path.title().split('\\')[0].split(maxsplit=1)

                if (cognome, nome) in lavoratori:
                    print('\n', cognome, nome)
                    lavoratore = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]
                    anagrafica = Anagrafica.objects.get(lavoratore__id=lavoratore.id)
                    formazione = Formazione.objects.get(lavoratore__id=lavoratore.id)
                    nomina = Nomine.objects.get(lavoratore__id=lavoratore.id)

                    for documento in files:
                        pth = os.path.join(root, documento)
                        mtime = os.stat(pth).st_mtime

                        # gg è il numero di giorni di vecchiaia del documento
                        gg = 14
                        if mtime >= ADESSO - gg * 24 * 60 * 60:
                            print('   ', documento)
                            documento = documento.lower()

                            if documento.endswith('.pdf'):
                                tipo, scadenza = documento.split()[:2]

                                if tipo == 'doc':
                                    formazione.ci = scadenza2date(documento, 0)

                                elif tipo in ('idoneità', 'idoneita'):
                                    anagrafica.idoneita = scadenza2date(documento, 0)

                                elif tipo == 'unilav':
                                    if scadenza == 'ind.pdf':
                                        anagrafica.indeterminato = True
                                        anagrafica.unilav = None
                                    else:
                                        anagrafica.unilav = scadenza2date(documento, 0)

                                elif tipo in ('art37', 'art.37'):
                                    formazione.art37 = scadenza2date(documento)

                                elif tipo in ('primo', 'primosoccorso', 'primo.soccorso'):
                                    formazione.primo_soccorso = scadenza2date(documento, 3)

                                elif tipo == 'antincendio':
                                    formazione.antincendio = scadenza2date(documento, 0)

                                elif tipo == 'preposto':
                                    formazione.preposto = scadenza2date(documento)

                                elif tipo in ('h2s.safety', 'h2s'):
                                    formazione.h2s = scadenza2date(documento)

                                elif tipo == 'dpi':
                                    formazione.dpi3 = scadenza2date(documento)

                                elif tipo in ('carrelli', 'carrello', 'sollevatore'):
                                    formazione.carrello = scadenza2date(documento)

                                elif tipo == 'ple':
                                    formazione.ple = scadenza2date(documento)

                                elif tipo in ('autogru', 'gru'):
                                    formazione.gru = scadenza2date(documento)

                                elif tipo == 'imbracatore':
                                    formazione.imbracatore = scadenza2date(documento)

                                elif tipo in (
                                        'spazi', 'spazio', 'spazio.confinato', 'spazi.confinato', 'spazi.confinati'):
                                    formazione.spazi_confinati = scadenza2date(documento)

                                elif tipo in ('altro', 'rir'):
                                    formazione.rir = scadenza2date(documento)

                                elif tipo == 'rls':
                                    formazione.rls = scadenza2date(documento, 1)

                                elif tipo == 'rspp':
                                    formazione.rspp = scadenza2date(documento)

                                elif tipo == 'ponteggi':
                                    formazione.ponteggi = scadenza2date(documento, 4)

                                elif tipo == 'lavori.quota':
                                    formazione.lavori_quota = scadenza2date(documento, 5)

                                elif tipo == 'nomina.preposto':
                                    nomina.preposto = scadenza2date(documento, 0)

                                elif tipo == 'nomina.antincendio':
                                    nomina.antincendio = scadenza2date(documento, 0)

                                elif tipo == 'nomina.primo.soccorso':
                                    nomina.primo_soccorso = scadenza2date(documento, 0)

                                elif tipo == 'nomina.rls':
                                    nomina.rls = scadenza2date(documento, 0)

                                elif tipo == 'nomina.aspp':
                                    nomina.aspp = scadenza2date(documento, 0)

                                else:
                                    print('***', tipo, '+++', cognome, nome, documento)

                            formazione.save()
                            anagrafica.save()
                            nomina.save()

            except ValueError:
                print('*** Errore in ', path)


def aggiorna_elenco_lavoratori():
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
                        Lavoratore.objects.get(cognome=cognome, nome=nome)
                    except Lavoratore.DoesNotExist:
                        lavoratore = Lavoratore(cognome=cognome, nome=nome)
                        lavoratore.save()
                        print('Nuovo Lavoratore: ', lavoratore)

        primo_ciclo = False

    lavoratori = Lavoratore.objects.all()
    for lavoratore in lavoratori:
        # crea la formazione per ogni lavoratore
        res = Formazione.objects.filter(lavoratore__id=lavoratore.id)

        if len(res) == 0:
            formazione = Formazione(lavoratore=lavoratore)
            formazione.save()
            print('Nuova Formazione: ', lavoratore)

        # crea anagrafica per ogni lavoratore
        res = Anagrafica.objects.filter(lavoratore__id=lavoratore.id)

        if len(res) == 0:
            anagrafica = Anagrafica(lavoratore=lavoratore)
            anagrafica.in_forza = True
            anagrafica.azienda = 'm'
            anagrafica.save()
            print('Nuova Anagrafica: ', lavoratore)

        # crea nomine per ogni lavoratore
        res = Nomine.objects.filter(lavoratore__id=lavoratore.id)

        if len(res) == 0:
            nomina = Nomine(lavoratore=lavoratore)
            nomina.save()
            print('Nuova Nomina: ', lavoratore)


def data_ultima_modifica_scrivi():
    with open(FILE_DATA_ULTIMA_MODIFICA, 'w') as fout:
        fout.write('%s' % OGGI)


def data_ultima_modifica_leggi():
    with open(FILE_DATA_ULTIMA_MODIFICA, 'r') as fin:
        data = fin.read()
        data = datetime.datetime.strptime(data, "%Y-%m-%d")
        return data.strftime("%d/%m/%y")
