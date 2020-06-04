import pandas as pd
import datetime

from personale.models import Lavoratore

PROGRAMMA_OFFICINA = 'Programma Officina.xlsx'

MANSIONI = {
    'a. carpentiere in ferro': 'A.CARP',
    'a. tubista': 'A.TUB',
    'aiutante': 'AIUT',
    'capo squadra': 'CS',
    'carpentiere in ferro': 'CARP',
    'tubista': 'TUB',
}


def idoneita(data):
    dt = (data - datetime.date.today()).days

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

    elenco_lavoratori =[]
    lavoratori = pd.read_excel(PROGRAMMA_OFFICINA, sheet_name='lavoratori', na_values=1).fillna('').values.tolist()
    # print(lavoratori)
    for cognome, nome, scheda, cs in lavoratori:
        res = Lavoratore.objects.get(cognome=cognome.strip(), nome=nome.strip())
        lavoratore = {'nome': '%s %s' % (res.cognome, res.nome), 'azienda': res.azienda.nome[0],
                      'mansione': MANSIONI[res.mansione.lower()], 'idoneita': idoneita(res.idoneita)}
        elenco_lavoratori.append(lavoratore)

        if cs:
            # schede[scheda]['cs'] = '%s %s' % (cognome.strip(), nome[:3])
            schede[scheda]['cs'] = lavoratore
        else:
            # schede[scheda]['lavoratori'].append('%s %s' % (cognome.strip(), nome[:3]))
            schede[scheda]['lavoratori'].append(lavoratore)


    return schede, elenco_lavoratori
