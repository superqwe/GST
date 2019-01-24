import datetime

from django.contrib import admin

from personale import admin_actions
from personale.models import Lavoratore, Cantiere, Azienda

OGGI = datetime.date.today()
DT = datetime.timedelta(30)
DT_6_MESI = datetime.timedelta(30 * 6)
AVVISO_SCADENZA = OGGI + DT
AVVISO_SCADENZA_ATTESTATI = OGGI + DT_6_MESI
PATH_BASE = "C:\\Users\\leonardo.masi\\Documents\\Personale"


# azioni lavoratore

def aggiorna_stato_lavoratori(modeladmin, request, queryset):
    admin_actions.aggiorna_stato_lavoratori()
    admin_actions.data_ultima_modifica_scrivi()


def rinomina_attestati(modeladmin, request, queryset):
    admin_actions.rinomina_attestati()


def aggiorna_scadenza_documenti(modeladmin, request, queryset):
    admin_actions.aggiorna_scadenza_documenti()
    admin_actions.data_ultima_modifica_scrivi()


def aggiorna_elenco_lavoratori(modeladmin, request, queryset):
    admin_actions.aggiorna_elenco_lavoratori()
    admin_actions.data_ultima_modifica_scrivi()


def esporta_dati(modeladmin, request, queryset):
    admin_actions.esporta_dati()


def importa_dati(modeladmin, request, queryset):
    admin_actions.importa_dati()


def aaa(modeladmin, request, queryset):
    Lavoratore.objects.filter(in_forza=True, azienda='m').update(azienda2=Azienda.objects.get(nome='Modomec'))
    Lavoratore.objects.filter(in_forza=True, azienda='b').update(azienda2=Azienda.objects.get(nome='Building'))
    Lavoratore.objects.filter(in_forza=True, azienda='r').update(azienda2=Azienda.objects.get(nome='Rimec'),
                                                                 cantiere2=Cantiere.objects.get(nome='Massafra'))
    Lavoratore.objects.filter(in_forza=True, azienda='w').update(azienda2=Azienda.objects.get(nome='Welding'))

    Lavoratore.objects.filter(in_forza=True, cantiere='sede').update(cantiere2=Cantiere.objects.get(nome='Massafra'))
    Lavoratore.objects.filter(in_forza=True, cantiere='ilva_ta').update(
        cantiere2=Cantiere.objects.get(nome='ArcelorMittal'))
    Lavoratore.objects.filter(in_forza=True, cantiere='andritz_ch').update(
        cantiere2=Cantiere.objects.get(nome='Andritz'))
    Lavoratore.objects.filter(in_forza=True, cantiere='appia_ta').update(cantiere2=Cantiere.objects.get(nome='Appia'))
    Lavoratore.objects.filter(in_forza=True, cantiere='ve').update(cantiere2=Cantiere.objects.get(nome='Marghera'))



aggiorna_stato_lavoratori.short_description = "Aggiorna Stato"
rinomina_attestati.short_description = "Rinomina Documenti"
aggiorna_scadenza_documenti.short_description = "Aggiorna Documenti"
aggiorna_elenco_lavoratori.short_description = "Aggiorna Elenco"
esporta_dati.short_description = "Esporta Dati"
importa_dati.short_description = "Importa Dati"


@admin.register(Azienda)
class AziendaAdmin(admin.ModelAdmin):
    pass


@admin.register(Cantiere)
class CantiereAdmin(admin.ModelAdmin):
    pass


@admin.register(Lavoratore)
class LavoratoreAdmin(admin.ModelAdmin):
    actions = [aggiorna_elenco_lavoratori,
               aggiorna_scadenza_documenti,
               aggiorna_stato_lavoratori,
               rinomina_attestati,
               esporta_dati,
               importa_dati,
               aaa]

    list_display = ('cognome', 'nome', 'mansione', 'stato', 'in_forza', 'azienda', 'azienda2', 'cantiere', 'cantiere2',
                    'idoneita', 'indeterminato', 'unilav')
    ordering = ['cognome', 'nome']
    search_fields = ['cognome', 'nome']
    list_filter = ['in_forza', 'azienda', 'cantiere', 'stato', 'indeterminato']
