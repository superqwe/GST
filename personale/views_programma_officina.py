import datetime

import pandas as pd
import numpy as np

from pprint import pprint as pp
from personale.models import Lavoratore

N_CARD_PER_RIGO = 7
N_COLONNE_ELENCO_LAVORATORI = 3
TRONCA_NOME = 15
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
    schede = {x[0]: {'commesse': [], 'lavoratori': [], 'cs': None, 'tipo_scheda': x[1]} for x in schede}
    pp(schede)

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
            schede[scheda]['cs'] = lavoratore
        else:
            schede[scheda]['lavoratori'].append(lavoratore)

    elenco_lavoratori.sort()
    elenco_lavoratori = [lavoratore for nome, lavoratore in elenco_lavoratori]
    # n_lav = len(elenco_lavoratori)
    # n = n_lav // N_COLONNE_ELENCO_LAVORATORI + n_lav % N_COLONNE_ELENCO_LAVORATORI
    # elenco_lavoratori_1 = elenco_lavoratori[:n]
    # elenco_lavoratori_2 = elenco_lavoratori[n:]

    elenco_lavoratori = np.array_split(elenco_lavoratori, N_COLONNE_ELENCO_LAVORATORI)

    # suddivisione schede in righi
    righe = []
    rigo = {}
    for n, scheda in enumerate(schede):

        if n % N_CARD_PER_RIGO == 0:

            if rigo:
                righe.append(rigo)

            rigo = {}

        rigo[scheda] = schede[scheda]

    # inserimento caselle vuote per riempimento ultimo rigo
    for x in range(N_CARD_PER_RIGO - n % N_CARD_PER_RIGO - 1):
        rigo[x] = {}

    righe.append(rigo)

    # TODO rimuovere shede dal return
    # return schede, (elenco_lavoratori_1, elenco_lavoratori_2), righe
    return elenco_lavoratori, righe
