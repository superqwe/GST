from django.db import models

STATO = (('v', 'Verde'),
         ('g', 'Giallo'),
         ('r', 'Rosso'),
         (None, '-'))


class Azienda(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '%s' % self.nome

    class Meta:
        ordering = ['nome', ]
        verbose_name = 'Azienda'
        verbose_name_plural = 'Aziende'


class Cantiere(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '%s' % self.nome

    class Meta:
        ordering = ['nome', ]
        verbose_name = 'Cantiere'
        verbose_name_plural = 'Cantieri'


class Lavoratore(models.Model):
    FOTO = (('v', 'Variabile'),
            ('640x480', 'ENI_TA'),
            (None, '-'),
            )

    # anagrafica
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)

    in_forza = models.BooleanField(default=False, verbose_name='In Forza')
    azienda = models.ForeignKey('Azienda', default=1, on_delete=models.CASCADE)
    stato = models.CharField(null=True, blank=True, max_length=1, choices=STATO)

    cantiere = models.ForeignKey('Cantiere', default=1, on_delete=models.CASCADE)
    mansione = models.CharField(max_length=50, null=True, blank=True, verbose_name='Mansione')

    ci = models.DateField(null=True, blank=True, verbose_name="CI")
    codice_fiscale = models.CharField(max_length=16, null=True, blank=True, verbose_name='Codice Fiscale')
    foto = models.CharField(max_length=10, default=None, null=True, blank=True, choices=FOTO, verbose_name='Foto')
    idoneita = models.DateField(null=True, blank=True, verbose_name='Idoneità')

    indeterminato = models.BooleanField(default=False, verbose_name='Inderminato')
    unilav = models.DateField(null=True, blank=True, verbose_name='UNILAV')
    data_assunzione = models.DateField(null=True, blank=True, verbose_name='Data Assunzione')
    data_nascita = models.DateField(null=True, blank=True, verbose_name='Data Nascita')
    luogo_nascita = models.CharField(max_length=100, null=True, blank=True, verbose_name='Luogo Nascita')
    luogo_residenza = models.CharField(max_length=100, null=True, blank=True, verbose_name='Luogo Residenza')

    # formazione
    art37 = models.DateField(null=True, blank=True, verbose_name='Art.37')
    primo_soccorso = models.DateField(null=True, blank=True, verbose_name='Primo Soccorso')
    antincendio = models.DateField(null=True, blank=True)
    preposto = models.DateField(null=True, blank=True)
    dirigente = models.DateField(null=True, blank=True)

    h2s = models.DateField(null=True, blank=True, verbose_name='H2S')
    dpi3 = models.DateField(null=True, blank=True, verbose_name='DPI3')
    apvr = models.DateField(null=True, blank=True, verbose_name='APVR')

    carrello = models.DateField(null=True, blank=True, verbose_name='Muletto')
    escavatore = models.DateField(null=True, blank=True, verbose_name='Escavatore')
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
    nomina_preposto = models.DateField(null=True, blank=True, verbose_name='Nomina Preposto')
    nomina_antincendio = models.DateField(null=True, blank=True, verbose_name='Nomina Antincendio')
    nomina_primo_soccorso = models.DateField(null=True, blank=True, verbose_name='Nomina Primo Soccorso')
    nomina_rls = models.DateField(null=True, blank=True, verbose_name='Nomina RLS')
    nomina_aspp = models.DateField(null=True, blank=True, verbose_name='Nomina ASPP')

    # varie
    consegna_dpi = models.DateField(null=True, blank=True, verbose_name="Consegna DPI")

    def __str__(self):
        return '%s %s' % (self.cognome, self.nome)

    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name = 'Lavoratore'
        verbose_name_plural = 'Lavoratori'


class Simulazione_Emergenza(models.Model):
    data = models.DateField(null=True, blank=True, verbose_name='Data Esercitazione')
    emergenza = models.CharField(max_length=100, null=True, blank=True, )
    area = models.CharField(max_length=100, null=True, blank=True, )
    partecipanti = models.ManyToManyField(Lavoratore)

    class Meta:
        ordering = ['data', ]
        verbose_name = 'Simulazione Emergenza'
        verbose_name_plural = 'Simulazioni Emergenza'

    def __str__(self):
        return '%s | %s | %s' % (self.data, self.emergenza, self.area)
