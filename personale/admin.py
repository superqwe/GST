import datetime
import os
import re

from django.contrib import admin

from .models import Lavoratore

import pandas as pd

from pprint import pprint as pp


def scadenza2date(documento):
    re_dma = re.compile(r'\d{2}\.\d{2}\.\d{2,4}')
    try:
        giorno, mese, anno = re_dma.findall(documento)[0].split('.')
        anno = int(anno) if len(anno) == 4 else int(anno) + 2000
        scadenza = datetime.date(anno, int(mese), int(giorno))
        return scadenza
    except IndexError:
        print('+++', documento)
        return None


def aggiorna_lavoratori(modeladmin, request, queryset):
    path_base = r'C:\Users\HP\Desktop\Sicurezza2\Personale'

    print('*' * 450)

    primo_ciclo = True
    for root, dirs, files in os.walk(path_base):

        for lavoratore in dirs:
            lavoratore = lavoratore.strip().title().split()

            if lavoratore[0] != 'Z':
                if primo_ciclo:
                    print(lavoratore)
                    cognome, nome = lavoratore

                    try:
                        res = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]
                    except IndexError:
                        lavoratore = Lavoratore(cognome=cognome, nome=nome)
                        lavoratore.save()

        primo_ciclo = False


def aggiorna_attestati(modeladmin, request, queryset):
    path_base = r'C:\Users\HP\Desktop\Sicurezza2\Personale'
    re_dma = re.compile(r'\d{2}\.\d{2}\.\d{2,4}')

    for root, dirs, files in os.walk(path_base):
        path = root[len(path_base) + 1:].lower()

        if not path.startswith('z ') and not 'scaduti' in root:
            try:
                cognome, nome = path.title().split('\\')[0].split()
                print('\n', cognome, nome)
                lavoratore = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]

                salva = False
                for documento in files:
                    documento = documento.lower()

                    if documento.endswith('.pdf'):
                        tipo, scadenza = documento.split()[:2]

                        # if cognome == 'Clemente' and nome == 'Mario':
                        #     print(documento, '-->', tipo)

                        if tipo == 'doc':
                            scadenza = scadenza2date(documento)
                            lavoratore.ci = scadenza

                        elif tipo == 'idoneità':
                            scadenza = scadenza2date(documento)
                            lavoratore.idoneita = scadenza

                        elif tipo == 'unilav':
                            scadenza = scadenza2date(documento)
                            lavoratore.unilav = scadenza

                        elif tipo in ('art37', 'art.37'):
                            scadenza = scadenza2date(documento)
                            lavoratore.art37 = scadenza

                        elif tipo in ('primosoccorso', 'primo.soccorso'):
                            scadenza = scadenza2date(documento)
                            lavoratore.primo_soccorso = scadenza

                        elif tipo == 'antincendio':
                            scadenza = scadenza2date(documento)
                            lavoratore.antincendio = scadenza

                        elif tipo == 'preposto':
                            scadenza = scadenza2date(documento)
                            lavoratore.preposto = scadenza

                        elif tipo in ('h2s.safety', 'h2s'):
                            scadenza = scadenza2date(documento)
                            lavoratore.h2s = scadenza

                        elif tipo == 'dpi':
                            scadenza = scadenza2date(documento)
                            lavoratore.dpi3 = scadenza

                        elif tipo in ('carrelli', 'sollevatore'):
                            scadenza = scadenza2date(documento)
                            lavoratore.carrello = scadenza

                        elif tipo == 'ple':
                            scadenza = scadenza2date(documento)
                            lavoratore.ple = scadenza

                        elif tipo in ('autogru', 'gru'):
                            scadenza = scadenza2date(documento)
                            lavoratore.gru = scadenza

                        elif tipo == 'imbracatore':
                            scadenza = scadenza2date(documento)
                            lavoratore.imbracatore = scadenza

                        elif tipo in ('spazi', 'spazio', 'spazio.confinato'):
                            scadenza = scadenza2date(documento)
                            lavoratore.spazi_confinati = scadenza

                        elif tipo in ('altro', 'rir'):
                            scadenza = scadenza2date(documento)
                            lavoratore.rir = scadenza

                        elif tipo == 'rspp':
                            scadenza = scadenza2date(documento)
                            lavoratore.rspp = scadenza

                        else:
                            print('***', tipo, '+++', documento)

                lavoratore.save()

            except ValueError:
                pass


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




aggiorna_lavoratori.short_description = "Aggiorna Lavoratori"
aggiorna_attestati.short_description = "Aggiorna Documenti"
aggiorna_gst.short_description = "Aggiorna GST"


class LavoratoreAdmin(admin.ModelAdmin):
    actions = [aggiorna_lavoratori, aggiorna_attestati, aggiorna_gst]
    list_display = ('cognome', 'nome',
                    'in_cantiere',
                    'situazione', 'gst',
                    'rait', 'ci', 'idoneita', 'unilav',
                    'art37', 'primo_soccorso', 'antincendio', 'preposto',
                    'h2s', 'dpi3',
                    'carrello', 'ple', 'gru', 'imbracatore',
                    'spazi_confinati',
                    'rir', 'rspp')

    ordering = ['cognome', 'nome']


admin.site.register(Lavoratore, LavoratoreAdmin)
