import datetime
import os
import re
from pprint import pprint as pp

import pandas as pd

from personale.models import Anagrafica, Formazione, Lavoratore

OGGI = datetime.date.today()
DT = datetime.timedelta(30)
DT_6_MESI = datetime.timedelta(30 * 6)
AVVISO_SCADENZA = OGGI + DT
AVVISO_SCADENZA_ATTESTATI = OGGI + DT_6_MESI
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

    # crea anagrafica per ogni lavoratore
    lavoratori = Lavoratore.objects.all()

    for lavoratore in lavoratori:
        res = Anagrafica.objects.filter(lavoratore__id=lavoratore.id)

        # break

        if len(res) == 0:
            anagrafica = Anagrafica(lavoratore=lavoratore)
            anagrafica.save()
            print('Nuova Anagrafica: ', lavoratore)


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
                anagrafica = Anagrafica.objects.get(lavoratore__id=lavoratore.id)

                for documento in files:
                    documento = documento.lower()

                    if documento.endswith('.pdf'):
                        tipo, scadenza = documento.split()[:2]

                        if tipo == 'doc':
                            scadenza = scadenza2date(documento, 0)
                            formazione.ci = scadenza

                        elif tipo in ('idoneità', 'idoneita'):
                            scadenza = scadenza2date(documento, 0)
                            anagrafica.idoneita = scadenza

                        elif tipo == 'unilav':
                            if scadenza == 'ind.pdf':
                                anagrafica.indeterminato = True
                                anagrafica.unilav = None
                            else:
                                scadenza = scadenza2date(documento, 0)
                                anagrafica.unilav = scadenza

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

                        elif tipo in ('spazi', 'spazio', 'spazio.confinato', 'spazi.confinato', 'spazi.confinati'):
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

                        elif tipo == 'lavori.quota':
                            scadenza = scadenza2date(documento, 5)
                            formazione.lavori_quota = scadenza

                        else:
                            print('***', tipo, '+++', cognome, nome, documento)

                formazione.save()
                anagrafica.save()

            except ValueError:
                print('*** Errore in ', path)


def aggiorna_stato_anagrafica():
    lavoratori = Anagrafica.objects.filter(in_forza=True)

    for lavoratore in lavoratori:
        stato = 'v'

        if lavoratore.idoneita and lavoratore.idoneita < AVVISO_SCADENZA or lavoratore.unilav and lavoratore.unilav < AVVISO_SCADENZA:
            stato = 'g'

        if not lavoratore.idoneita or lavoratore.idoneita and lavoratore.idoneita < OGGI or lavoratore.unilav and lavoratore.unilav < OGGI:
            stato = 'r'

        lavoratore.stato = stato
        lavoratore.save()

    Anagrafica.objects.filter(in_forza=False).update(stato=None, azienda=None)

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

def rinomina_attestati():
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

                    if scadenza:
                        da = os.path.join(PATH_BASE, path, documento)
                        a = os.path.join(PATH_BASE, path, '%s %s.pdf' % (tipo, scadenza))
                        os.rename(da, a)
                    else:
                        print(cognome, nome)

            except ValueError:
                print('*** Errore in ', path)

def in_sede(queryset):
    for lavoratore in queryset:
        lavoratore.cantiere = 'sede'
        lavoratore.save()

def in_ilva(queryset):
    for lavoratore in queryset:
        lavoratore.cantiere = 'ilva_ta'
        lavoratore.save()

def no_cantiere(queryset):
    for lavoratore in queryset:
        lavoratore.cantiere = None
        lavoratore.save()

def in_forza(queryset):
    for lavoratore in queryset:
        lavoratore.in_forza = True
        lavoratore.save()

def azienda_m(queryset):
    for lavoratore in queryset:
        lavoratore.azienda = 'm'
        lavoratore.save()

def azienda_nessuna(queryset):
    for lavoratore in queryset:
        lavoratore.azienda = None
        lavoratore.save()

def aggiorna_stato_formazione():
    campi = Formazione._meta.get_fields()[3:]

    lavoratori = Anagrafica.objects.filter(in_forza=True)

    for lavoratore in lavoratori:
        lavoratore = Formazione.objects.get(lavoratore=lavoratore.lavoratore)

        stato = 'v'

        for campo in campi:

            if campo.name != 'antincendio':

                try:
                    if getattr(lavoratore, campo.name) < OGGI:
                        print(campo.name, getattr(lavoratore, campo.name))
                        stato = 'r'
                        break
                    elif getattr(lavoratore, campo.name) < AVVISO_SCADENZA_ATTESTATI:
                        stato = 'g'

                except TypeError:
                    pass

        lavoratore.stato_formazione = stato
        lavoratore.save()

def esporta_mansioni():
    lavoratori = Anagrafica.objects.all().order_by('lavoratore')

    dati = []
    for lavoratore in lavoratori:
        rigo = (lavoratore.lavoratore.cognome, lavoratore.lavoratore.nome, lavoratore.mansione)
        dati.append(rigo)

    dati = pd.DataFrame(dati, columns=('cognome', 'nome', 'mansione'))

    dati.to_excel('mansioni.xlsx', sheet_name='mansioni')
    print('\n*** Mansioni esportate\n')

def importa_mansioni():
    xlsx = pd.ExcelFile('mansioni.xlsx')
    df = pd.read_excel(xlsx, 'mansioni')

    for n, cognome, nome, mansione in df.itertuples():
        if type(mansione) == str:
            lavoratore = Anagrafica.objects.get(lavoratore__cognome=cognome, lavoratore__nome=nome)
            lavoratore.mansione = mansione
            lavoratore.save()


def aggiorna_stato_lavoratori():
    aggiorna_stato_anagrafica()
    aggiorna_stato_formazione()