import datetime
import os
import re
import time

import pandas as pd

from personale.models import Lavoratore, Azienda, Cantiere

ADESSO = time.time()
OGGI = datetime.date.today()
DT = datetime.timedelta(30)
DT_6_MESI = datetime.timedelta(30 * 6)

AVVISO_SCADENZA = OGGI + DT
AVVISO_SCADENZA_ATTESTATI = OGGI + DT_6_MESI

PATH_BASE = "C:\\Users\\leonardo.masi\\Documents\\Personale"
FILE_DATI = 'dati.xlsx'
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


def rinomina_attestati():
    # todo obsoleto da aggiornare
    path_base = PATH_BASE
    print('*' * 400)

    for root, dirs, files in os.walk(path_base):
        path = root[len(path_base) + 1:].lower()

        if not path.startswith('z ') and not 'scaduti' in root:
            try:
                cognome, nome = path.title().split('\\')[0].split(maxsplit=1)
                print('\n', cognome, nome)
                lavoratore = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]
                # formazione = Formazione.objects.get(lavoratore__id=lavoratore.id)

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

    lavoratori = Lavoratore.objects.filter(in_forza=True).values_list('cognome', 'nome')

    for root, dirs, files in os.walk(path_base):
        path = root[len(path_base) + 1:].lower()

        if not path.startswith('z ') and not 'scaduti' in root:
            try:
                cognome, nome = path.title().split('\\')[0].split(maxsplit=1)

                if (cognome, nome) in lavoratori:
                    print('\n', cognome, nome)
                    lavoratore = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]

                    for documento in files:
                        pth = os.path.join(root, documento)
                        mtime = os.stat(pth).st_mtime

                        # gg è il numero di giorni di vecchiaia del documento
                        gg = 7
                        if mtime >= ADESSO - gg * 24 * 60 * 60:
                            print('   ', documento)
                            documento = documento.lower()

                            if documento.endswith('.pdf'):
                                tipo, scadenza = documento.split()[:2]

                                if tipo == 'doc':
                                    lavoratore.ci = scadenza2date(documento, 0)

                                elif tipo in ('idoneità', 'idoneita'):
                                    lavoratore.idoneita = scadenza2date(documento, 0)

                                elif tipo == 'unilav':
                                    if scadenza == 'ind.pdf':
                                        lavoratore.indeterminato = True
                                        lavoratore.unilav = None
                                    else:
                                        lavoratore.unilav = scadenza2date(documento, 0)

                                elif tipo in ('art37', 'art.37'):
                                    lavoratore.art37 = scadenza2date(documento)

                                elif tipo in ('primo', 'primosoccorso', 'primo.soccorso'):
                                    lavoratore.primo_soccorso = scadenza2date(documento, 3)

                                elif tipo == 'antincendio':
                                    lavoratore.antincendio = scadenza2date(documento, 0)

                                elif tipo == 'preposto':
                                    lavoratore.preposto = scadenza2date(documento)

                                elif tipo in ('h2s.safety', 'h2s'):
                                    lavoratore.h2s = scadenza2date(documento)

                                elif tipo == 'dpi':
                                    lavoratore.dpi3 = scadenza2date(documento)

                                elif tipo in ('carrelli', 'carrello', 'sollevatore'):
                                    lavoratore.carrello = scadenza2date(documento)

                                elif tipo == 'ple':
                                    lavoratore.ple = scadenza2date(documento)

                                elif tipo in ('autogru', 'gru'):
                                    lavoratore.gru = scadenza2date(documento)

                                elif tipo == 'imbracatore':
                                    lavoratore.imbracatore = scadenza2date(documento)

                                elif tipo in (
                                        'spazi', 'spazio', 'spazio.confinato', 'spazi.confinato', 'spazi.confinati'):
                                    lavoratore.spazi_confinati = scadenza2date(documento)

                                elif tipo in ('altro', 'rir'):
                                    lavoratore.rir = scadenza2date(documento)

                                elif tipo == 'rls':
                                    lavoratore.rls = scadenza2date(documento, 1)

                                elif tipo == 'rspp':
                                    lavoratore.rspp = scadenza2date(documento)

                                elif tipo == 'ponteggi':
                                    lavoratore.ponteggi = scadenza2date(documento, 4)

                                elif tipo == 'lavori.quota':
                                    lavoratore.lavori_quota = scadenza2date(documento, 5)

                                elif tipo == 'nomina.preposto':
                                    lavoratore.nomina_preposto = scadenza2date(documento, 0)

                                elif tipo == 'nomina.antincendio':
                                    lavoratore.nomina_antincendio = scadenza2date(documento, 0)

                                elif tipo == 'nomina.primo.soccorso':
                                    lavoratore.nomina_primo_soccorso = scadenza2date(documento, 0)

                                elif tipo == 'nomina.rls':
                                    lavoratore.nomina_rls = scadenza2date(documento, 0)

                                elif tipo == 'nomina.aspp':
                                    lavoratore.nomina_aspp = scadenza2date(documento, 0)

                                else:
                                    print('***', tipo, '+++', cognome, nome, documento)

                            lavoratore.save()

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


def data_ultima_modifica_scrivi():
    with open(FILE_DATA_ULTIMA_MODIFICA, 'w') as fout:
        fout.write('%s' % OGGI)


def data_ultima_modifica_leggi():
    with open(FILE_DATA_ULTIMA_MODIFICA, 'r') as fin:
        data = fin.read()
        data = datetime.datetime.strptime(data, "%Y-%m-%d")
        return data.strftime("%d/%m/%y")


def esporta_dati():
    lavoratori = Lavoratore.objects.all()

    dati = []
    for lavoratore in lavoratori:
        rigo = (lavoratore.cognome, lavoratore.nome, lavoratore.mansione, lavoratore.in_forza,
                lavoratore.azienda, lavoratore.cantiere)
        dati.append(rigo)

    dati = pd.DataFrame(dati, columns=('cognome', 'nome', 'mansione', 'in_forza', 'azienda', 'cantiere'))

    dati.to_excel(FILE_DATI, sheet_name='dati')

    print('\n*** Dati anagrafici esportati\n')


def importa_dati():
    xlsx = pd.ExcelFile(FILE_DATI)
    df = pd.read_excel(xlsx, 'dati')
    df = df.where((pd.notnull(df)), None)

    for n, cognome, nome, mansione, in_forza, azienda, cantiere in df.itertuples():
        if type(mansione) == str:
            lavoratore = Lavoratore.objects.get(cognome=cognome, nome=nome)
            lavoratore.mansione = mansione
            lavoratore.in_forza = in_forza
            lavoratore.azienda = Azienda.objects.get(nome=azienda)
            lavoratore.cantiere = Cantiere.objects.get(nome=cantiere)

            lavoratore.save()

    print('\n*** Dati anagrafici importati\n')


def aggiorna_stato_lavoratori():
    campi_formazione = ('art37', 'primo_soccorso', 'antincendio', 'preposto', 'h2s', 'dpi3', 'carrello', 'ple', 'gru',
                        'imbracatore', 'ponteggi', 'lavori_quota', 'spazi_confinati', 'rir', 'rls', 'rspp')
    lavoratori = Lavoratore.objects.filter(in_forza=True)

    for lavoratore in lavoratori:
        stato = 'v'

        if lavoratore.idoneita and lavoratore.idoneita < AVVISO_SCADENZA or lavoratore.unilav and lavoratore.unilav < AVVISO_SCADENZA:
            stato = 'g'

        if not lavoratore.idoneita or lavoratore.idoneita and lavoratore.idoneita < OGGI or lavoratore.unilav and lavoratore.unilav < OGGI:
            stato = 'r'
        else:

            for campo in campi_formazione:

                if campo != 'antincendio':

                    try:
                        if getattr(lavoratore, campo) < OGGI:
                            print(campo, getattr(lavoratore, campo))
                            stato = 'r'
                            break
                        elif getattr(lavoratore, campo) < AVVISO_SCADENZA_ATTESTATI:
                            stato = 'g'

                    except TypeError:
                        pass

        lavoratore.stato = stato
        lavoratore.save()

    Lavoratore.objects.filter(in_forza=False).update(stato=None, azienda=Azienda.objects.get(nome='-'))
