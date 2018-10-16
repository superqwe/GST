import os

from django.contrib import admin

from .models import Lavoratore


def aggiorna_lavoratori(modeladmin, request, queryset):
    path_base = r'C:\Users\HP\Desktop\Sicurezza2\Personale'

    primo_ciclo = True
    for root, dirs, files in os.walk(path_base):
        path = root[len(path_base) + 1:]

        if primo_ciclo:
            for lavoratore in dirs:
                lavoratore = lavoratore.strip().title().split()

                if lavoratore[0] != 'Z':
                    cognome, nome = lavoratore
                    try:
                        res = Lavoratore.objects.filter(cognome=cognome, nome=nome)[0]
                    except IndexError:
                        lavoratore = Lavoratore(cognome=cognome, nome=nome)
                        lavoratore.save()

            primo_ciclo = False


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
