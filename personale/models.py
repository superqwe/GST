from django.db import models

STATO = (('v', 'Verde'),
         ('g', 'Giallo'),
         ('r', 'Rosso'),
         ('c', 'Grigio'))


# Create your models here.
class Lavoratore(models.Model):
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.cognome, self.nome)

    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name = 'Lavoratore'
        verbose_name_plural = 'Lavoratori'


class Formazione(models.Model):
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE)
    stato_formazione = models.CharField(null=True, blank=True, max_length=1, choices=STATO,
                                        verbose_name='Stato Formazione')
    art37 = models.DateField(null=True, blank=True, verbose_name='Art.37')
    primo_soccorso = models.DateField(null=True, blank=True, verbose_name='Primo Soccorso')
    antincendio = models.DateField(null=True, blank=True)
    preposto = models.DateField(null=True, blank=True)

    h2s = models.DateField(null=True, blank=True, verbose_name='H2S')
    dpi3 = models.DateField(null=True, blank=True, verbose_name='DPI3')

    carrello = models.DateField(null=True, blank=True, verbose_name='Muletto')
    ple = models.DateField(null=True, blank=True, verbose_name='PLE')
    gru = models.DateField(null=True, blank=True)
    imbracatore = models.DateField(null=True, blank=True)

    ponteggi = models.DateField(null=True, blank=True, verbose_name='Ponteggi')
    lavori_quota = models.DateField(null=True, blank=True, verbose_name='Lavori in Quota')
    spazi_confinati = models.DateField(null=True, blank=True, verbose_name='Spazi Confinati')

    rir = models.DateField(null=True, blank=True, verbose_name='RIR')
    rls = models.DateField(null=True, blank=True, verbose_name='RLS')
    rspp = models.DateField(null=True, blank=True, verbose_name='RSPP')

    def __str__(self):
        return '%s' % self.lavoratore

    class Meta:
        verbose_name = 'Formazione'
        verbose_name_plural = 'Formazione'


class Anagrafica(models.Model):
    SITUAZIONE_GST = (('v', 'Verde'),
                      ('g', 'Giallo'),
                      ('r', 'Rosso'))

    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE)
    stato = models.CharField(null=True, blank=True, max_length=1, choices=STATO)

    in_cantiere = models.BooleanField(default=True, verbose_name='In Cantiere')

    codice_fiscale = models.CharField(max_length=16, null=True, blank=True, verbose_name='Codice Fiscale')

    situazione = models.CharField(null=True, blank=True, max_length=1, choices=SITUAZIONE_GST,
                                  verbose_name='Situazione GST')
    gst = models.DateField(null=True, blank=True, verbose_name='GST')

    rait = models.DateField(null=True, blank=True, verbose_name='RAIT')
    ci = models.DateField(null=True, blank=True, verbose_name="CI")
    idoneita = models.DateField(null=True, blank=True, verbose_name='Idoneità')
    unilav = models.DateField(null=True, blank=True, verbose_name='UNILAV')

    # def __str__(self):
    #     return '%s %s' % (self.cognome, self.nome)

    class Meta:
        verbose_name = 'Anagrafica'
        verbose_name_plural = 'Anagrafica'
