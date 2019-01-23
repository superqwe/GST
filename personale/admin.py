import datetime
from pprint import pprint as pp

import pandas as pd
from django.contrib import admin

from personale import admin_actions_formazione, admin_actions_lavoratore, admin_actions_anagrafica
from personale.models import Anagrafica, Formazione, Lavoratore, Nomine

OGGI = datetime.date.today()
DT = datetime.timedelta(30)
DT_6_MESI = datetime.timedelta(30 * 6)
AVVISO_SCADENZA = OGGI + DT
AVVISO_SCADENZA_ATTESTATI = OGGI + DT_6_MESI
PATH_BASE = "C:\\Users\\leonardo.masi\\Documents\\Personale"


# azioni lavoratore

def aggiorna_stato_lavoratori(modeladmin, request, queryset):
    admin_actions_lavoratore.aggiorna_stato_lavoratori()
    admin_actions_lavoratore.data_ultima_modifica_scrivi()


def rinomina_attestati(modeladmin, request, queryset):
    admin_actions_lavoratore.rinomina_attestati()


def aggiorna_scadenza_documenti(modeladmin, request, queryset):
    admin_actions_lavoratore.aggiorna_scadenza_documenti()
    admin_actions_lavoratore.data_ultima_modifica_scrivi()


def aggiorna_elenco_lavoratori(modeladmin, request, queryset):
    admin_actions_lavoratore.aggiorna_elenco_lavoratori()
    admin_actions_lavoratore.data_ultima_modifica_scrivi()


aggiorna_stato_lavoratori.short_description = "Aggiorna Stato"
rinomina_attestati.short_description = "Rinomina Documenti"
aggiorna_scadenza_documenti.short_description = "Aggiorna Documenti"
aggiorna_elenco_lavoratori.short_description = "Aggiorna Elenco"


# azioni formazione


def aggiorna_stato_formazione(modeladmin, request, queryset):
    admin_actions_formazione.aggiorna_stato_formazione()


aggiorna_stato_formazione.short_description = "Aggiorna Stato"


# azioni anagrafica

def azienda(modeladmin, request, queryset):
    admin_actions_anagrafica.azienda_m(queryset)


def azienda_nessuna(modeladmin, request, queryset):
    admin_actions_anagrafica.azienda_nessuna(queryset)


def in_forza(modeladmin, request, queryset):
    admin_actions_anagrafica.in_forza(queryset)


def in_sede(modeladmin, request, queryset):
    admin_actions_anagrafica.in_sede(queryset)


def in_ilva(modeladmin, request, queryset):
    admin_actions_anagrafica.in_ilva(queryset)


def no_cantiere(modeladmin, request, queryset):
    admin_actions_anagrafica.no_cantiere(queryset)


def aggiorna_stato_anagrafica(modeladmin, request, queryset):
    admin_actions_anagrafica.aggiorna_stato_anagrafica()


def esporta_dati(modeladmin, request, queryset):
    admin_actions_anagrafica.esporta_dati()


def importa_dati(modeladmin, request, queryset):
    admin_actions_anagrafica.importa_dati()


azienda_nessuna.short_description = "Nessuna azienda"
in_forza.short_description = "In Forza"
in_sede.short_description = "In Sede"
in_ilva.short_description = "In Ilva"
no_cantiere.short_description = "Nessun Cantiere"
no_cantiere.aggiorna_anagrafica = "Nessun Cantiere"
esporta_dati.short_description = "Esporta Dati"
importa_dati.short_description = "Importa Dati"


class AnagraficaAdmin(admin.ModelAdmin):
    actions = [aggiorna_stato_anagrafica,
               esporta_dati,
               importa_dati,
               # in_sede,
               # in_ilva,
               # no_cantiere,
               # in_forza,
               # azienda_m,
               # azienda_nessuna,
               ]
    list_display = ('lavoratore', 'stato', 'codice_fiscale',
                    'in_forza', 'azienda', 'cantiere', 'mansione',
                    'idoneita', 'indeterminato', 'unilav')
    list_filter = ['in_forza', 'stato', 'azienda', 'cantiere', 'indeterminato']
    ordering = ['lavoratore']
    search_fields = ['lavoratore__cognome', ]


class FormazioneAdmin(admin.ModelAdmin):
    actions = [aggiorna_stato_formazione,
               ]
    list_display = ('lavoratore', 'stato',
                    'art37',
                    'preposto', 'primo_soccorso', 'antincendio',
                    'dpi3', 'ponteggi', 'lavori_quota',
                    'carrello', 'ple', 'gru', 'imbracatore',
                    'spazi_confinati', 'h2s',
                    'rir', 'rls', 'rspp')
    list_filter = ['stato', ]
    ordering = ['lavoratore']
    search_fields = ['lavoratore__cognome', ]


@admin.register(Lavoratore)
class LavoratoreAdmin(admin.ModelAdmin):
    actions = [aggiorna_elenco_lavoratori,
               aggiorna_scadenza_documenti,
               aggiorna_stato_lavoratori,
               rinomina_attestati,
               esporta_dati,
               importa_dati,
               ]

    list_display = ('cognome', 'nome', 'mansione', 'in_forza', 'idoneita', 'indeterminato', 'unilav')
    ordering = ['cognome', 'nome']
    search_fields = ['cognome', 'nome']
    list_filter = ['in_forza', 'azienda', 'cantiere', 'indeterminato']


class NomineAdmin(admin.ModelAdmin):
    list_display = ('lavoratore', 'preposto', 'antincendio', 'primo_soccorso', 'rls', 'aspp')
    ordering = ['lavoratore']
    search_fields = ['lavoratore__cognome', ]


admin.site.register(Anagrafica, AnagraficaAdmin)
admin.site.register(Formazione, FormazioneAdmin)
admin.site.register(Nomine, NomineAdmin)
