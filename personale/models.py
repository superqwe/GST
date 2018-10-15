from django.db import models

# Create your models here.
class Lavoratore(models.Model):
    # in_cantiere =
    cognome = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    codice_fiscale = models.CharField(max_length=16)
    # rait = models.DateField()
    # ci =
    # idoneita =
    # unilav =
    # art37 =
    # primo_soccorso
    # antincendio
    # preposto
    # h2s =
    # dpi3
    # carrello
    # ple
    # gru
    # imbracatore
    # spazi_confinati
    # rir
    # rspp
