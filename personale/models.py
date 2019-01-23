from django.db import models

STATO = (('v', 'Verde'),
         ('g', 'Giallo'),
         ('r', 'Rosso'),
         (None, '-'))


# Create your models here.
class Lavoratore(models.Model):
    SITUAZIONE_GST = (('v', 'Verde'),
                      ('g', 'Giallo'),
                      ('r', 'Rosso'))
    CANTIERE = (('sede', 'Massafra'),
                ('ilva_ta', 'ArcelorMittal'),
                ('andritz_ch', 'Andritz'),
                ('ve', 'Marghera'),
                ('eni_ta', 'Raffineria'),
                (None, '-')  # non in forza
                )
    AZIENDA = (('m', 'M'),
               ('b', 'B'),
               ('r', 'R'),
               ('w', 'W'),
               (None, '-')
               )

    # anagrafica
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)

    in_forza = models.BooleanField(default=False, verbose_name='In Forza')
    azienda = models.CharField(null=True, blank=True, max_length=2, choices=AZIENDA)
    stato = models.CharField(null=True, blank=True, max_length=1, choices=STATO)

    cantiere = models.CharField(max_length=10, null=True, blank=True, choices=CANTIERE, verbose_name='Cantiere')
    mansione = models.CharField(max_length=30, null=True, blank=True, verbose_name='Mansione')

    ci = models.DateField(null=True, blank=True, verbose_name="CI")
    codice_fiscale = models.CharField(max_length=16, null=True, blank=True, verbose_name='Codice Fiscale')
    idoneita = models.DateField(null=True, blank=True, verbose_name='Idoneità')
    indeterminato = models.BooleanField(default=False, verbose_name='Inderminato')
    unilav = models.DateField(null=True, blank=True, verbose_name='UNILAV')

    # formazione
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

    # nomine
    nomina_preposto = models.DateField(null=True, blank=True, verbose_name='Preposto')
    nomina_antincendio = models.DateField(null=True, blank=True, verbose_name='Antincendio')
    nomina_primo_soccorso = models.DateField(null=True, blank=True, verbose_name='Primo Soccorso')
    nomina_rls = models.DateField(null=True, blank=True, verbose_name='RLS')
    nomina_aspp = models.DateField(null=True, blank=True, verbose_name='ASPP')

    def __str__(self):
        return '%s %s' % (self.cognome, self.nome)

    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name = 'Lavoratore'
        verbose_name_plural = 'Lavoratori'
