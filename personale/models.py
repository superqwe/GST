from django.db import models


# Create your models here.
class Lavoratore(models.Model):
    in_cantiere =models.BooleanField(default=True)

    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    codice_fiscale = models.CharField(max_length=16, null=True, blank=True)

    rait = models.DateField(null=True, blank=True)
    ci = models.DateField(null=True, blank=True)
    idoneita = models.DateField(null=True, blank=True)
    unilav = models.DateField(null=True, blank=True)

    art37 = models.DateField(null=True, blank=True)
    primo_soccorso = models.DateField(null=True, blank=True)
    antincendio = models.DateField(null=True, blank=True)
    preposto = models.DateField(null=True, blank=True)

    h2s = models.DateField(null=True, blank=True)
    dpi3 = models.DateField(null=True, blank=True)

    carrello = models.DateField(null=True, blank=True)
    ple = models.DateField(null=True, blank=True)
    gru = models.DateField(null=True, blank=True)
    imbracatore = models.DateField(null=True, blank=True)

    spazi_confinati = models.DateField(null=True, blank=True)

    rir = models.DateField(null=True, blank=True)
    rspp = models.DateField(null=True, blank=True)
