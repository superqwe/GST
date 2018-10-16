from django.db import models


# Create your models here.
class Lavoratore(models.Model):
    in_cantiere = models.BooleanField(default=True, verbose_name='In Cantiere')

    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    codice_fiscale = models.CharField(max_length=16, null=True, blank=True, verbose_name='Codice Fiscale')

    rait = models.DateField(null=True, blank=True, verbose_name='RAIT')
    ci = models.DateField(null=True, blank=True, verbose_name="CI")
    idoneita = models.DateField(null=True, blank=True, verbose_name='Idoneità')
    unilav = models.DateField(null=True, blank=True, verbose_name='UNILAV')

    art37 = models.DateField(null=True, blank=True)
    primo_soccorso = models.DateField(null=True, blank=True, verbose_name='Primo Soccorso')
    antincendio = models.DateField(null=True, blank=True)
    preposto = models.DateField(null=True, blank=True)

    h2s = models.DateField(null=True, blank=True, verbose_name='H2S')
    dpi3 = models.DateField(null=True, blank=True, verbose_name='DPI3')

    carrello = models.DateField(null=True, blank=True, verbose_name='Muletto')
    ple = models.DateField(null=True, blank=True, verbose_name='PLE')
    gru = models.DateField(null=True, blank=True)
    imbracatore = models.DateField(null=True, blank=True)

    spazi_confinati = models.DateField(null=True, blank=True, verbose_name='Spazi Confinati')

    rir = models.DateField(null=True, blank=True, verbose_name='RIR')
    rspp = models.DateField(null=True, blank=True, verbose_name='RSPP')

    def __str__(self):
        return '%s %s' % (self.cognome, self.nome)

    class Meta:
        verbose_name = 'Lavoratore'
        verbose_name_plural = 'Lavoratori'
