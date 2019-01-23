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


def aggiorna_stato_formazione():
    campi = Formazione._meta.get_fields()[3:]
    pp(campi)
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
