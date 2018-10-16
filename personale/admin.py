import datetime
import os
import re

from django.contrib import admin

from .models import Lavoratore


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
                            mese, anno = scadenza.split('.')
                            ci = datetime.date(int(anno), int(mese), 1)
                            lavoratore.ci = ci
                            salva = True

                        elif tipo == 'idoneità':
                            mese, anno = scadenza.split('.')
                            scadenza = datetime.date(int(anno), int(mese), 1)
                            lavoratore.idoneita = scadenza
                            salva = True

                        elif tipo == 'unilav':
                            giorno, mese, anno = scadenza.split('.')
                            anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                            scadenza = datetime.date(anno, int(mese), int(giorno))
                            lavoratore.unilav = scadenza
                            salva = True


                        elif tipo in ('art37', 'art.37'):
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.art37 = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo in ('primosoccorso', 'primo.soccorso'):
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.primo_soccorso = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'antincendio':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.antincendio = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'preposto':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.preposto = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo in ('h2s.safety', 'h2s'):
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.h2s = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'dpi':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.dpi3 = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo in ('carrelli', 'sollevatore'):
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.carrello = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'ple':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.ple = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo in ('autogru', 'gru'):
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.gru = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'imbracatore':
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.imbracatore = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo in ('spazi', 'spazio', 'spazio.confinato'):
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.spazi_confinati = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo in ('altro', 'rir'):
                            try:
                                giorno, mese, anno = re_dma.findall(documento)[0].split('.')
                                anno = int(anno) if len(anno) == 4 else int(anno) + 2000
                                scadenza = datetime.date(anno, int(mese), int(giorno))
                                lavoratore.rir = scadenza
                                salva = True
                            except IndexError:
                                print('+++', documento)

                        elif tipo == 'rspp':
                            scadenza = scadenza2date(documento)
                            lavoratore.rspp = scadenza
                            if scadenza:  salva = True

                        else:
                            print('***', tipo, '+++', documento)

                if salva:
                    lavoratore.save()

            except ValueError:
                pass

        # print()


aggiorna_lavoratori.short_description = "Aggiorna Lavoratori"
aggiorna_attestati.short_description = "Aggiorna Attestati"


class LavoratoreAdmin(admin.ModelAdmin):
    actions = [aggiorna_lavoratori, aggiorna_attestati]
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
