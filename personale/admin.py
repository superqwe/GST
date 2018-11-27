import datetime
from pprint import pprint as pp

import pandas as pd
from django.contrib import admin

from personale import admin_actions
from personale.models import Anagrafica, Formazione, Lavoratore

OGGI = datetime.date.today()
DT = datetime.timedelta(30)
DT_6_MESI = datetime.timedelta(30 * 6)
AVVISO_SCADENZA = OGGI + DT
AVVISO_SCADENZA_ATTESTATI = OGGI + DT_6_MESI
PATH_BASE = "C:\\Users\\leonardo.masi\\Documents\\Personale"


def aggiorna_lavoratori(modeladmin, request, queryset):
    admin_actions.aggiorna_lavoratori()


def aggiorna_stato_lavoratori(modeladmin, request, queryset):
    admin_actions.aggiorna_stato_lavoratori()


aggiorna_lavoratori.short_description = "Aggiorna Elenco Lavoratori"
aggiorna_stato_lavoratori.short_description = "Aggiorna Stato Lavoratori"


# azioni formazione

def aggiorna_attestati(modeladmin, request, queryset):
    admin_actions.aggiorna_attestati()


def rinomina_attestati(modeladmin, request, queryset):
    admin_actions.rinomina_attestati()


def aggiorna_stato_formazione(modeladmin, request, queryset):
    admin_actions.aggiorna_stato_formazione()


aggiorna_attestati.short_description = "Aggiorna Documenti Lavoratori"
rinomina_attestati.short_description = "Rinomina Documenti Lavoratori"
aggiorna_stato_formazione.short_description = "Aggiorna Stato"


# azioni anagrafica

def azienda(modeladmin, request, queryset):
    admin_actions.azienda_m(queryset)


def azienda_nessuna(modeladmin, request, queryset):
    admin_actions.azienda_nessuna(queryset)


def in_forza(modeladmin, request, queryset):
    admin_actions.in_forza(queryset)


def in_sede(modeladmin, request, queryset):
    admin_actions.in_sede(queryset)


def in_ilva(modeladmin, request, queryset):
    admin_actions.in_ilva(queryset)


def no_cantiere(modeladmin, request, queryset):
    admin_actions.no_cantiere(queryset)


def aggiorna_stato_anagrafica(modeladmin, request, queryset):
    admin_actions.aggiorna_stato_anagrafica()


def esporta_mansioni(modeladmin, request, queryset):
    admin_actions.esporta_mansioni()


def importa_mansioni(modeladmin, request, queryset):
    admin_actions.importa_mansioni()


azienda_nessuna.short_description = "Nessuna azienda"
in_forza.short_description = "In Forza"
in_sede.short_description = "In Sede"
in_ilva.short_description = "In Ilva"
no_cantiere.short_description = "Nessun cantiere"
no_cantiere.aggiorna_anagrafica = "Nessun cantiere"
esporta_mansioni.short_description = "Esporta Mansioni"
importa_mansioni.short_description = "Importa Mansioni"


class AnagraficaAdmin(admin.ModelAdmin):
    actions = [
        # in_sede,
        # in_ilva,
        # no_cantiere,
        # in_forza,
        aggiorna_lavoratori,
        aggiorna_stato_anagrafica,
        # azienda_nessuna,
        esporta_mansioni,
        importa_mansioni,
    ]
    list_display = ('lavoratore', 'stato',
                    'in_forza', 'azienda', 'cantiere', 'mansione',
                    'idoneita', 'unilav')
    list_filter = ['in_forza', 'stato', 'azienda', 'cantiere']
    ordering = ['lavoratore']
    search_fields = ['lavoratore__cognome', ]


class FormazioneAdmin(admin.ModelAdmin):
    actions = [aggiorna_lavoratori,
               aggiorna_attestati,
               rinomina_attestati,
               aggiorna_stato_formazione]
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


class LavoratoreAdmin(admin.ModelAdmin):
    actions = [aggiorna_lavoratori,
               aggiorna_attestati,
               aggiorna_stato_lavoratori,
               rinomina_attestati,
               esporta_mansioni,
               importa_mansioni,
               ]

    list_display = ('cognome', 'nome', 'stato')
    # list_filter = ['stato', ]
    ordering = ['cognome', 'nome']
    search_fields = ['cognome', 'nome']


admin.site.register(Anagrafica, AnagraficaAdmin)
admin.site.register(Formazione, FormazioneAdmin)
admin.site.register(Lavoratore, LavoratoreAdmin)
