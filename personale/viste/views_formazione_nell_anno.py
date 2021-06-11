import os
from pprint import pprint as pp

from GST.settings import STATIC_ROOT

ANNO = '21'


def formazione_nell_anno():
    path_base = r'C:\Users\leonardo.masi\Documents\Personale'
    elenco_lavoratori = os.listdir(path_base)

    elenco_attestati = []
    for lavoratore in elenco_lavoratori:
        path_attestati_lavoratore = os.path.join(path_base, lavoratore, 'attestati')

        if os.path.exists(path_attestati_lavoratore):
            attestati = os.listdir(path_attestati_lavoratore)

            for attestato in attestati:
                attestato = os.path.splitext(attestato)[0]
                if attestato.endswith(ANNO):
                    corso, data = attestato.split()
                    data = data[-2:] + data[2:-2] + data[:2]
                    attestato = ('%s %s' % (data, corso))
                    elenco_attestati.append(attestato)

    elenco_attestati.sort()

    elenco_corsi = list(set(elenco_attestati))
    elenco_corsi.sort()

    conteggio_corsi = []
    for corso in elenco_corsi:
        n = elenco_attestati.count(corso)
        data, corso = corso.split()
        data = data[-2:] + data[2:-2] + data[:2]
        conteggio_corsi.append(('%i %s %s' % (n, data, corso)))

    return conteggio_corsi
