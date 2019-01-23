import datetime

from django.contrib import admin

from personale import admin_actions
from personale.models import Lavoratore

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


aggiorna_stato_lavoratori.short_description = "Aggiorna Stato"
rinomina_attestati.short_description = "Rinomina Documenti"
aggiorna_scadenza_documenti.short_description = "Aggiorna Documenti"
aggiorna_elenco_lavoratori.short_description = "Aggiorna Elenco"
esporta_dati.short_description = "Esporta Dati"
importa_dati.short_description = "Importa Dati"


# azioni formazione


# def aggiorna_stato_formazione(modeladmin, request, queryset):
#     admin_actions_formazione.aggiorna_stato_formazione()
#
#
# aggiorna_stato_formazione.short_description = "Aggiorna Stato"


# azioni anagrafica

# def azienda(modeladmin, request, queryset):
#     admin_actions_anagrafica.azienda_m(queryset)
#
#
# def azienda_nessuna(modeladmin, request, queryset):
#     admin_actions_anagrafica.azienda_nessuna(queryset)
#
#
# def in_forza(modeladmin, request, queryset):
#     admin_actions_anagrafica.in_forza(queryset)
#
#
# def in_sede(modeladmin, request, queryset):
#     admin_actions_anagrafica.in_sede(queryset)
#
#
# def in_ilva(modeladmin, request, queryset):
#     admin_actions_anagrafica.in_ilva(queryset)
#
#
# def no_cantiere(modeladmin, request, queryset):
#     admin_actions_anagrafica.no_cantiere(queryset)
#
#
# def aggiorna_stato_anagrafica(modeladmin, request, queryset):
#     personale.admin_actions.aggiorna_stato_anagrafica()
#
#
# azienda_nessuna.short_description = "Nessuna azienda"
# in_forza.short_description = "In Forza"
# in_sede.short_description = "In Sede"
# in_ilva.short_description = "In Ilva"
# no_cantiere.short_description = "Nessun Cantiere"
# no_cantiere.aggiorna_anagrafica = "Nessun Cantiere"


@admin.register(Lavoratore)
class LavoratoreAdmin(admin.ModelAdmin):
    actions = [aggiorna_elenco_lavoratori,
               aggiorna_scadenza_documenti,
               aggiorna_stato_lavoratori,
               rinomina_attestati,
               esporta_dati,
               importa_dati,
               ]

    list_display = ('cognome', 'nome', 'mansione', 'stato', 'in_forza', 'azienda', 'cantiere', 'idoneita',
                    'indeterminato', 'unilav')
    ordering = ['cognome', 'nome']
    search_fields = ['cognome', 'nome']
    list_filter = ['in_forza', 'azienda', 'cantiere', 'stato', 'indeterminato']
