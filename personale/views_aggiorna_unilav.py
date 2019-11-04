from pprint import pprint as pp

from django.core.exceptions import ObjectDoesNotExist

from personale.models import Azienda, Lavoratore, Cantiere


def assunzione(nominativi):
    errori = []
    for nominativo in nominativi:
        cognome, nome, cf, data_assunzione, data_scadenza = nominativo

        try:
            lavoratore = Lavoratore.objects.get(cognome=cognome, nome=nome)
            lavoratore.codice_fiscale = cf
            lavoratore.data_assunzione = data_assunzione
            lavoratore.unilav = data_scadenza
            lavoratore.save()
        except ObjectDoesNotExist:
            print('errore', nominativo)
            errori.append(('%s %s' % (cognome, nome), 'Lavoratore non trovato'))

    return errori
