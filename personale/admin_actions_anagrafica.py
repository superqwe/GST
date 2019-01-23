import datetime

from personale.models import Anagrafica

OGGI = datetime.date.today()
DT = datetime.timedelta(30)
DT_6_MESI = datetime.timedelta(30 * 6)
AVVISO_SCADENZA = OGGI + DT
AVVISO_SCADENZA_ATTESTATI = OGGI + DT_6_MESI
PATH_BASE = "C:\\Users\\leonardo.masi\\Documents\\Personale"

FILE_DATI = 'dati.xlsx'


def in_sede(queryset):
    for lavoratore in queryset:
        lavoratore.cantiere = 'sede'
        lavoratore.save()


def in_ilva(queryset):
    for lavoratore in queryset:
        lavoratore.cantiere = 'ilva_ta'
        lavoratore.save()


def no_cantiere(queryset):
    for lavoratore in queryset:
        lavoratore.cantiere = None
        lavoratore.save()


def in_forza(queryset):
    for lavoratore in queryset:
        lavoratore.in_forza = True
        lavoratore.save()


def azienda_m(queryset):
    for lavoratore in queryset:
        lavoratore.azienda = 'm'
        lavoratore.save()


def azienda_nessuna(queryset):
    for lavoratore in queryset:
        lavoratore.azienda = None
        lavoratore.save()


def aggiorna_stato_anagrafica():
    lavoratori = Anagrafica.objects.filter(in_forza=True)

    for lavoratore in lavoratori:
        stato = 'v'

        if lavoratore.idoneita and lavoratore.idoneita < AVVISO_SCADENZA or lavoratore.unilav and lavoratore.unilav < AVVISO_SCADENZA:
            stato = 'g'

        if not lavoratore.idoneita or lavoratore.idoneita and lavoratore.idoneita < OGGI or lavoratore.unilav and lavoratore.unilav < OGGI:
            stato = 'r'

        lavoratore.stato = stato
        lavoratore.save()

    Anagrafica.objects.filter(in_forza=False).update(stato=None, azienda=None)
