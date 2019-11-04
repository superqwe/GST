import os
from pprint import pprint as pp

from django.core.exceptions import ObjectDoesNotExist

from personale.models import Azienda, Lavoratore, Cantiere

def rinomina_unilav(lavoratore):
    cartella_iniziale = os.getcwd()
    cartella_personale = 'C:\Users\leonardo.masi\Documents\Personale'


def assunzione(nominativi):
    errori = []
    print('\nAssunzione')
    for nominativo in nominativi:
        cognome, nome, cf, data_assunzione, data_scadenza = nominativo

        try:
            lavoratore = Lavoratore.objects.get(cognome=cognome, nome=nome)
            print(lavoratore)
        except ObjectDoesNotExist:
            lavoratore = Lavoratore(cognome=cognome, nome=nome)
            lavoratore.save()
            print(lavoratore, '---> nuovo')

        lavoratore.codice_fiscale = cf
        lavoratore.data_assunzione = data_assunzione
        lavoratore.unilav = data_scadenza
        lavoratore.in_forza = True
        lavoratore.azienda = Azienda.objects.get(nome='Modomec')
        lavoratore.save()

        rinomina_unilav(lavoratore)

    return errori
