import glob
import os
import shutil

from django.core.exceptions import ObjectDoesNotExist

from personale.models import Azienda, Lavoratore


def rinomina_unilav(lavoratore, indeterminato=None):
    # cartella_iniziale = os.getcwd()
    cartella_personale = r'C:\Users\leonardo.masi\Documents\Personale'

    nominativo = '%s %s' % (lavoratore.cognome, lavoratore.nome)

    cartella_lavoratore = os.path.join(cartella_personale, nominativo)
    cartella_scaduti = os.path.join(cartella_lavoratore, 'scaduti')

    lista_unilav = glob.glob('%s/u*' % cartella_lavoratore)

    if lista_unilav:
        for unilav_path in lista_unilav:
            unilav = os.path.split(unilav_path)[1].split()

            if len(unilav) == 2:
                data_file = os.path.splitext(unilav[1])[0]

                if data_file == 'ind':
                    pass

                elif lavoratore.indeterminato or data_file != lavoratore.unilav.strftime('%d%m%y'):

                    if not os.path.isdir(cartella_scaduti):
                        os.mkdir(cartella_scaduti)

                    try:
                        shutil.move(unilav_path, cartella_scaduti)
                        print('--> unilav spostato in scaduti')
                    except:
                        os.remove(unilav_path)
                        print('--> unilav vecchio esistente in scaduti')

            else:
                data = 'ind' if indeterminato else lavoratore.unilav.strftime('%d%m%y')
                unilav_rinominato = '%s\\unilav %s.pdf' % (cartella_lavoratore, data)
                shutil.move(unilav_path, unilav_rinominato)
                print('--> unilav rinominato')


    else:
        print('*** ERRORE --> UNILAV NON PRESENTE')
        return True


def assunzione(nominativi):
    errori = []
    print('\nASSUNZIONE <--')

    for nominativo in nominativi:
        cognome, nome, cf, data_assunzione, data_scadenza = nominativo

        try:
            lavoratore = Lavoratore.objects.get(cognome=cognome, nome=nome)
            print(lavoratore)
        except ObjectDoesNotExist:
            lavoratore = Lavoratore(cognome=cognome, nome=nome)
            lavoratore.save()
            print(lavoratore, '\t---> nuovo')

        lavoratore.codice_fiscale = cf
        lavoratore.data_assunzione = data_assunzione
        lavoratore.unilav = data_scadenza

        if not data_scadenza:
            lavoratore.indeterminato = True

        lavoratore.in_forza = True
        lavoratore.azienda = Azienda.objects.get(nome='Modomec')
        lavoratore.save()

        if rinomina_unilav(lavoratore, lavoratore.indeterminato):
            errori.append(('%s %s' % (lavoratore.cognome, lavoratore.nome), 'UNILAV non presente'))

    return errori


def proroga(nominativi):
    errori = []
    print('\nPROROGA <--')

    for nominativo in nominativi:
        cognome, nome, cf, data_assunzione, data_scadenza = nominativo

        try:
            lavoratore = Lavoratore.objects.get(cognome=cognome, nome=nome)
            print(lavoratore)
        except ObjectDoesNotExist:
            lavoratore = Lavoratore(cognome=cognome, nome=nome)
            lavoratore.save()
            print(lavoratore, '\t---> nuovo')

        lavoratore.codice_fiscale = cf
        lavoratore.data_assunzione = data_assunzione
        lavoratore.unilav = data_scadenza
        lavoratore.in_forza = True
        lavoratore.azienda = Azienda.objects.get(nome='Modomec')
        lavoratore.save()

        if rinomina_unilav(lavoratore):
            errori.append(('%s %s' % (lavoratore.cognome, lavoratore.nome), 'UNILAV non presente'))

    return errori


def cessazione(nominativi):
    errori = []
    print('\nCESSAZIONE <--')

    for nominativo in nominativi:
        cognome, nome, cf, data_assunzione, data_cessazione = nominativo

        try:
            lavoratore = Lavoratore.objects.get(cognome=cognome, nome=nome)
            print(lavoratore)
        except ObjectDoesNotExist:
            lavoratore = Lavoratore(cognome=cognome, nome=nome)
            lavoratore.save()
            print(lavoratore, '\t---> nuovo')

        lavoratore.codice_fiscale = cf
        lavoratore.data_assunzione = data_assunzione
        lavoratore.unilav = data_cessazione
        lavoratore.in_forza = False
        lavoratore.indeterminato = False
        lavoratore.azienda = Azienda.objects.get(nome='-')
        lavoratore.save()

        if rinomina_unilav(lavoratore):
            errori.append(('%s %s' % (lavoratore.cognome, lavoratore.nome), 'UNILAV non presente'))

    return errori


def trasformazione(nominativi):
    errori = []
    print('\nTRASFORMAZIONE <--')

    for nominativo in nominativi:
        cognome, nome, cf, data_assunzione, data_trasformazione = nominativo

        try:
            lavoratore = Lavoratore.objects.get(cognome=cognome, nome=nome)
            print(lavoratore)
        except ObjectDoesNotExist:
            lavoratore = Lavoratore(cognome=cognome, nome=nome)
            lavoratore.save()
            print(lavoratore, '\t---> nuovo')

        lavoratore.codice_fiscale = cf
        lavoratore.data_assunzione = data_assunzione
        lavoratore.unilav = None
        lavoratore.in_forza = True
        lavoratore.indeterminato = True
        lavoratore.azienda = Azienda.objects.get(nome='Modomec')
        lavoratore.save()

        # lavoratore = Lavoratore.objects.filter(cognome=cognome, nome=nome).update(unilav=None)

        if rinomina_unilav(lavoratore, indeterminato=True):
            errori.append(('%s %s' % (lavoratore.cognome, lavoratore.nome), 'UNILAV non presente'))

    return errori
