from django.db import models

STATO = (('v', 'Verde'),
         ('g', 'Giallo'),
         ('r', 'Rosso'),
         (None, '-'))


# Create your models here.
class Lavoratore(models.Model):
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)

    def stato(self):
        anagrafica = Anagrafica.objects.get(lavoratore=self)

        if not anagrafica.in_forza:
            return '-'

        stato_anagrafica = anagrafica.stato
        stato_formazione = Formazione.objects.get(lavoratore=self).stato
        stati = (stato_anagrafica, stato_formazione)

        stato = 'v'
        if 'g' in stati:
            stato = 'g'
        if 'r' in stati:
            stato = 'r'

        return stato

    def __str__(self):
        return '%s %s' % (self.cognome, self.nome)

    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name = 'Lavoratore'
        verbose_name_plural = 'Lavoratori'


class Formazione(models.Model):
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE)
    stato = models.CharField(null=True, blank=True, max_length=1, choices=STATO,
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
    CANTIERE = (('sede', 'Massafra'),
                ('ilva_ta', 'Ilva'),
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

    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE)

    stato = models.CharField(null=True, blank=True, max_length=1, choices=STATO)

    in_forza = models.BooleanField(default=False, verbose_name='In Forza')
    azienda = models.CharField(null=True, blank=True, max_length=2, choices=AZIENDA)

    cantiere = models.CharField(max_length=10, null=True, blank=True, choices=CANTIERE, verbose_name='Cantiere')
    mansione = models.CharField(max_length=30, null=True, blank=True, verbose_name='Mansione')

    ci = models.DateField(null=True, blank=True, verbose_name="CI")
    codice_fiscale = models.CharField(max_length=16, null=True, blank=True, verbose_name='Codice Fiscale')
    idoneita = models.DateField(null=True, blank=True, verbose_name='Idoneità')
    indeterminato = models.BooleanField(default=False, verbose_name='Inderminato')
    unilav = models.DateField(null=True, blank=True, verbose_name='UNILAV')

    def __str__(self):
        return '%s ' % self.lavoratore

    class Meta:
        verbose_name = 'Anagrafica'
        verbose_name_plural = 'Anagrafica'


class Nomine(models.Model):
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE)
    preposto = models.DateField(null=True, blank=True, verbose_name='Preposto')
    antincendio = models.DateField(null=True, blank=True, verbose_name='Antincendio')
    primo_soccorso = models.DateField(null=True, blank=True, verbose_name='Primo Soccorso')
    rls = models.DateField(null=True, blank=True, verbose_name='RLS')
    aspp = models.DateField(null=True, blank=True, verbose_name='ASPP')

    def __str__(self):
        return '%s ' % self.lavoratore

    class Meta:
        verbose_name = 'Nomina'
        verbose_name_plural = 'Nomine'
