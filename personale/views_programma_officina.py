import datetime

import pandas as pd

from pprint import pprint as pp
from personale.models import Lavoratore

N_CARD_PER_RIGO = 5
PROGRAMMA_OFFICINA = 'Programma Officina.xlsx'
MANSIONI = {
    'a. carpentiere in ferro': 'A.CARP',
    'a. alesatore': 'OP MAC',
    'a. tubista': 'A.TUB',
    'a. verniciatore': 'A.VERN',
    'addetto alle pulizie': 'MANU',
    'addetto ufficio qualità': 'TEC',
    'aiutante': 'AIUT',
    'autista': 'AUT',
    'capo squadra': 'CS',
    'carpentiere in ferro': 'CARP',
    'carpentiere montatore': 'CARP',
    'centralinista telefonico': 'AMM',
    'conduttore macchine utensili': 'OP MAC',
    'elettricista': 'ELE',
    'elettrauto': 'ELE',
    'gruista': 'GRU',
    'impiegato tecnico': 'TEC',
    'impiegato tecnico supervisore': 'TEC',
    'impiegato amministrativo': 'AMM',
    'magazziniere': 'MAG',
    'manutentore meccanico': 'MEC',
    'meccanico': 'MEC',
    'operatore macchine utensili': 'OP MAC',
    'sabbiatore': 'SABB',
    'saldatore': 'SALD',
    'tornitore': 'OP MAC',
    'tubista': 'TUB',
    'verniciatore': 'VERN',
}


def idoneita(data):
    try:
        dt = (data - datetime.date.today()).days
    except TypeError:
        return 'table-danger'

    if dt < 0:
        return 'table-danger'
    elif dt <= 30:
        return 'table-warning'
    return 'table-success'


def programma_officina():
    schede = pd.read_excel(PROGRAMMA_OFFICINA, sheet_name='schede').values.tolist()
    schede = {x[0]: {'commesse': [], 'lavoratori': [], 'cs': None} for x in schede}
    # print(schede)

    commesse = pd.read_excel(PROGRAMMA_OFFICINA, sheet_name='commesse').values.tolist()
    # print(commesse)
    dummy = {schede[scheda]['commesse'].append(commessa) for (commessa, scheda) in commesse}

    elenco_lavoratori = []
    lavoratori = pd.read_excel(PROGRAMMA_OFFICINA, sheet_name='lavoratori', na_values=1).fillna('').values.tolist()
    # print(lavoratori)
    for cognome, nome, scheda, cs in lavoratori:
        res = Lavoratore.objects.get(cognome=cognome.strip(), nome=nome.strip())
        lavoratore = {'nome': '%s %s' % (res.cognome, res.nome), 'azienda': res.azienda.nome[0],
                      'mansione': MANSIONI[res.mansione.lower()], 'idoneita': idoneita(res.idoneita)}
        elenco_lavoratori.append(('%s %s' % (res.cognome, res.nome), lavoratore))

        if cs:
            # schede[scheda]['cs'] = '%s %s' % (cognome.strip(), nome[:3])
            schede[scheda]['cs'] = lavoratore
        else:
            # schede[scheda]['lavoratori'].append('%s %s' % (cognome.strip(), nome[:3]))
            schede[scheda]['lavoratori'].append(lavoratore)

    elenco_lavoratori.sort()
    elenco_lavoratori = [lavoratore for nome, lavoratore in elenco_lavoratori]
    n_lav = len(elenco_lavoratori)
    n = n_lav // 2 + n_lav % 2
    elenco_lavoratori_1 = elenco_lavoratori[:n]
    elenco_lavoratori_2 = elenco_lavoratori[n:]

    righe = []
    rigo = {}
    for n, scheda in enumerate(schede):

        if n % N_CARD_PER_RIGO == 0:

            if rigo:
                righe.append(rigo)

            rigo = {}

        rigo[scheda] = schede[scheda]

    righe.append(rigo)
    # pp(righe)
    return schede, (elenco_lavoratori_1, elenco_lavoratori_2), righe
