import datetime
import os
import re
from pprint import pprint as pp

import pandas as pd
from django.contrib import admin

from personale.models import Anagrafica, Formazione, Lavoratore
from personale.templates import admin_actions

OGGI = datetime.date.today()
DT = datetime.timedelta(30)
AVVISO_SCADENZA = OGGI + DT
PATH_BASE = "C:\\Users\\leonardo.masi\\Documents\\Personale"


def scadenza2date(documento, durata=5):
    re_dma = re.compile(r'\d{2}\.\d{2}\.\d{2,4}')

    if not re_dma.findall(documento):
        re_dma = re.compile(r'\d{6,8}')

        try:
            data = re_dma.findall(documento)[0]

            giorno, mese, anno = int(data[:2]), int(data[2:4]), int(data[4:])
            anno = anno if anno > 2000 else anno + 2000
            scadenza = datetime.date(anno + durata, mese, giorno)
            return scadenza
        except IndexError:
            print('+++', documento)
            return None

    try:
        giorno, mese, anno = re_dma.findall(documento)[0].split('.')
        anno = int(anno) if len(anno) == 4 else int(anno) + 2000
        scadenza = datetime.date(anno + durata, int(mese), int(giorno))
        return scadenza
    except IndexError:
        print('+++', documento)
        return None


def aggiorna_lavoratori(modeladmin, request, queryset):
    admin_actions.aggiorna_lavoratori()


def aggiorna_attestati(modeladmin, request, queryset):
    admin_actions.aggiorna_attestati()


def aggiorna_gst(modeladmin, request, queryset):
    fin = r'C:\Users\HP\Desktop\Sicurezza2\Personale\lavoratore.csv'
    csv = pd.read_csv(fin, sep=';', skiprows=1,
                      names=('cf', 'nome', 'cognome', 'punteggio', 'sospeso', 'data', 'situazione'))

    for row in csv.iterrows():
        cf, nome, cognome, punteggio, sospeso, data, situazione = row[1]

        res = Lavoratore.objects.filter(cognome=cognome.title(), nome=nome.title())

        if res:
            res[0].cf = cf
            res[0].gst = datetime.datetime.strptime(data, '%d-%m-%Y')
            res[0].situazione = situazione.lower()[0]
            res[0].save()


def aggiorna_rait(modeladmin, request, queryset):
    fin = r'C:\Users\HP\Desktop\Sicurezza2\Personale\rait.xlsx'
    xlsx = pd.read_excel(fin, header=0)

    for row in xlsx.iterrows():
        cognome, nome, data = row[1]
        res = Lavoratore.objects.filter(cognome=cognome.title(), nome=nome.title())

        if res and not pd.isnull(data):
            res[0].rait = data
            res[0].save()


def aggiorna_stato(modeladmin, request, queryset):
    campi = Lavoratore._meta.get_fields()[7:]

    lavoratori = Lavoratore.objects.all()

    for lavoratore in lavoratori:
        stato = 'v'

        if not lavoratore.in_cantiere:
            lavoratore.stato = 'c'
            lavoratore.save()
            continue

        if lavoratore.situazione in ('r', None):
            lavoratore.stato = 'r'
            lavoratore.save()
            continue

        for campo in campi:

            try:
                if getattr(lavoratore, campo.name) < OGGI:
                    stato = 'r'
                    break
                elif getattr(lavoratore, campo.name) < AVVISO_SCADENZA:
                    stato = 'g'

            except TypeError:
                pass

        if stato == 'r':
            lavoratore.save()
            continue

        # todo: da fare stato giallo
        if lavoratore.situazione in ('g', None):
            stato = 'g'

        lavoratore.stato = stato
        lavoratore.save()


aggiorna_lavoratori.short_description = "Aggiorna Elenco Lavoratori"
aggiorna_attestati.short_description = "Aggiorna Documenti Lavoratori"
aggiorna_gst.short_description = "Aggiorna GST"
aggiorna_rait.short_description = "Aggiorna RAIT"
aggiorna_stato.short_description = "Aggiorna Stato"


class FormazioneAdmin(admin.ModelAdmin):
    actions = [aggiorna_lavoratori, aggiorna_attestati]
    list_display = ('lavoratore', 'stato_formazione',
                    'art37',
                    'preposto', 'primo_soccorso', 'antincendio',
                    'dpi3', 'ponteggi',
                    'carrello', 'ple', 'gru', 'imbracatore',
                    'spazi_confinati', 'h2s',
                    'rir', 'rls', 'rspp')
    ordering = ['lavoratore']


class LavoratoreAdmin(admin.ModelAdmin):
    actions = [aggiorna_lavoratori, aggiorna_attestati, aggiorna_gst, aggiorna_rait, aggiorna_stato]

    list_display = ('cognome', 'nome')
    #                 'stato', 'stato_formazione', 'in_cantiere',
    #                 'situazione', 'gst', 'rait',
    #                 'ci', 'idoneita', 'unilav',

    ordering = ['cognome', 'nome']


admin.site.register(Anagrafica, )
admin.site.register(Formazione, FormazioneAdmin)
admin.site.register(Lavoratore, LavoratoreAdmin)
