from django.contrib import admin

from .models import Lavoratore


class LavoratoreAdmin(admin.ModelAdmin):
    fields = (('cognome', 'nome'), 'codice_fiscale')
    list_display = ('cognome', 'nome',
                    'in_cantiere',
                    'rait', 'ci', 'idoneita', 'unilav',
                    'art37','primo_soccorso','antincendio', 'preposto',
                    'h2s', 'dpi3',
                    'carrello', 'ple', 'gru', 'imbracatore',
                    'spazi_confinati',
                    'rir', 'rspp')
    pass


admin.site.register(Lavoratore, LavoratoreAdmin)
