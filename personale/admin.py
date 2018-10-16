import datetime
import os

from django.contrib import admin

from .models import Lavoratore
from pprint import pprint as pp
import re


def aggiorna_lavoratori(modeladmin, request, queryset):
    re_ma = re.compile('\d{2,2}.\d{2,4}')
    re_dma = re.compile('\d{2}\.\d{2}\.\d{2,4}')
    path_base = r'C:\Users\HP\Desktop\Sicurezza2\Personale'
    print('*' * 500)

    primo_ciclo = True
    for root, dirs, files in os.walk(path_base):
        path = root[len(path_base) + 1:].lower()

        # creazione nuovo Lavoratore
        for lavoratore in dirs:
            lavoratore = lavoratore.strip().title().split()

            if lavoratore[0] != 'Z':
                if primo_ciclo:
                    cognome, nome = lavoratore

                    try:
                        res = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]
                    except IndexError:
                        lavoratore = Lavoratore(cognome=cognome, nome=nome)
                        lavoratore.save()

                primo_ciclo = False

        # aggiornamento scadenze
        if not path.startswith('z ') and not 'scaduti' in root:
            try:
                cognome, nome = path.title().split('\\')[0].split()
                print('\n', cognome, nome)
                # print(files)
                lavoratore = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]

                # if cognome.lower() != 'allegrini':
                #     break

                for documento in files:
                    documento = documento.lower()
                    # print(documento)

                    if documento.endswith('.pdf'):
                        tipo, scadenza = documento.split()[:2]

                        if tipo == 'doc':
                            mese, anno = scadenza.split('.')
                            ci = datetime.date(int(anno), int(mese), 1)
                            lavoratore.ci = ci

                        elif tipo == 'idoneità':
                            mese, anno = scadenza.split('.')
                            scadenza = datetime.date(int(anno), int(mese), 1)
                            lavoratore.idoneita = scadenza

                        elif tipo == 'unilav':
                            giorno, mese, anno = scadenza.split('.')
                            anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                            scadenza = datetime.date(anno, int(mese), int(giorno))
                            lavoratore.unilav = scadenza

                        elif tipo == 'art.37':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.art37 = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'primosoccorso':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.primo_soccorso = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'antincendio':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.antincendio = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'preposto':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.preposto = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'h2s.safety':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.h2s = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'dpi':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.dpi3 = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'carrelli':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.carrello = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'ple':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.ple = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'autogru':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.gru = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'imbracatore':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.imbracatore = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'spazio':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.spazi_confinati = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'altro':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.rir = scadenza
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'rspp':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.rspp = scadenza
                            except IndexError:
                                print('+++', documento)

                        else:
                            print('***', tipo, '+++', documento)

                lavoratore.save()

            except ValueError:
                pass

        # print()


aggiorna_lavoratori.short_description = "Aggiorna Lavoratori"


class LavoratoreAdmin(admin.ModelAdmin):
    actions = [aggiorna_lavoratori, ]
    list_display = ('cognome', 'nome',
                    'in_cantiere',
                    'rait', 'ci', 'idoneita', 'unilav',
                    'art37', 'primo_soccorso', 'antincendio', 'preposto',
                    'h2s', 'dpi3',
                    'carrello', 'ple', 'gru', 'imbracatore',
                    'spazi_confinati',
                    'rir', 'rspp')

    ordering = ['cognome', 'nome']


admin.site.register(Lavoratore, LavoratoreAdmin)
