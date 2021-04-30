import dateutil.relativedelta
import pandas as pd
from django_pandas.io import read_frame

from personale.models import Lavoratore

FOUT = 'dimp.xlsx'


def dimp():
    lavoratori = Lavoratore.objects.filter(in_forza=True, cantiere__nome='Edison (VE)')

    pd_dati = read_frame(lavoratori)
    campi = ['cognome', 'nome', 'mansione', 'idoneità', 'art37', 'dpi3', 'apvr', 'lavori_quota', 'carrello', 'gru',
             'imbracatore', 'spazi_confinati', 'preposto', 'ple']
    pd_dati.drop(columns=[col for col in pd_dati if not col in campi], inplace=True)

    campi_da_calcolare_data_corso = ['art37', 'dpi3', 'apvr', 'lavori_quota', 'carrello', 'gru', 'imbracatore',
                                     'spazi_confinati', 'preposto', 'ple']
    for campo in campi_da_calcolare_data_corso:
        pd_dati['%s_fatto' % campo] = pd_dati[campo] + dateutil.relativedelta.relativedelta(years=-5)

    pd_dati.fillna(r'//', inplace=True)

    with pd.ExcelWriter(FOUT, engine='openpyxl') as writer:
        pd_dati.to_excel(writer)
        writer.save()
