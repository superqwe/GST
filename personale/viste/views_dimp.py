import dateutil.relativedelta
from django_pandas.io import read_frame

from personale.models import Lavoratore
from pprint import pprint as pp
import pandas as pd
import numpy as np

FOUT = 'dimp.xlsx'


def dimp():
    lavoratori = Lavoratore.objects.filter(in_forza=True, cantiere__nome='Edison (VE)')

    pd_dati = read_frame(lavoratori)
    campi = ['cognome', 'nome', 'mansione', 'idoneità', 'art37', 'dpi3', 'apvr', 'lavori_quota', 'carrello', 'gru',
             'imbracatore', 'spazi_confinati', 'preposto', 'ple']
    pd_dati.drop(columns=[col for col in pd_dati if not col in campi], inplace=True)

    campi = ['art37', 'dpi3', 'apvr', 'lavori_quota', 'carrello', 'gru', 'imbracatore', 'spazi_confinati', 'preposto',
             'ple']
    for campo in campi:
        pd_dati['%s_fatto' % campo] = pd_dati[campo] + dateutil.relativedelta.relativedelta(years=-5)
        # pd_dati[campo] = pd.to_datetime(pd_dati[campo], format="%d/%m/%Y", errors='ignore')

    pd_dati.fillna(r'//', inplace=True)

    print(pd_dati)

    with pd.ExcelWriter(FOUT, engine='openpyxl') as writer:
        pd_dati.to_excel(writer)
        writer.save()
