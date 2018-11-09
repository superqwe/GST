import datetime
import glob
import os
import shutil

import pandas as pd
from django.http import HttpResponse
from django.template import loader

from personale.models import Lavoratore, Formazione, Anagrafica
from personale.views_util import date_scadenza


def index(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")


def anagrafica(request):
    lavoratori = Anagrafica.objects.order_by('lavoratore')
    # lavoratori = Anagrafica.objects.filter(in_forza=True).order_by('lavoratore')

    nlavoratori = len(lavoratori)
    template = loader.get_template('personale/anagrafica.html')
    context = {
        'lavoratori': lavoratori,
        # 'lavoratori_per_cantiere': dati,
        'nlavoratori': nlavoratori,
        'oggi': date_scadenza()['oggi'],
        'mesi1': date_scadenza()['mesi1'],
        'mesi2': date_scadenza()['mesi2'],
        'mesi6': date_scadenza()['mesi6'],
        'mesi12': date_scadenza()['mesi12'],
    }
    return HttpResponse(template.render(context, request))


def anagrafica_per_cantiere(request):
    lavoratori = Anagrafica.objects.order_by('lavoratore')
    cantieri = Anagrafica.CANTIERE

    dati = []
    for cantiere in cantieri:
        lavoratori = Anagrafica.objects.filter(cantiere=cantiere[0]).order_by('lavoratore')

        dati.append((cantiere[1], lavoratori))

    template = loader.get_template('personale/anagrafica_per_cantiere.html')
    context = {
        'lavoratori': lavoratori,
        'lavoratori_per_cantiere': dati,
        'oggi': date_scadenza()['oggi'],
        'mesi1': date_scadenza()['mesi1'],
        'mesi2': date_scadenza()['mesi2'],
        'mesi6': date_scadenza()['mesi6'],
        'mesi12': date_scadenza()['mesi12'],
    }
    return HttpResponse(template.render(context, request))


def completo(request, filtro=False):
    dati = []
    lavoratori = Lavoratore.objects.order_by('cognome', 'nome')

    for lavoratore in lavoratori:
        anagrafica = Anagrafica.objects.get(lavoratore=lavoratore)
        formazione = Formazione.objects.get(lavoratore=lavoratore)

        if filtro == 'in_forza':
            if anagrafica.in_forza:
                dati.append((lavoratore, anagrafica, formazione))
        else:
            dati.append((lavoratore, anagrafica, formazione))

    nlavoratori = len(dati)

    template = loader.get_template('personale/completo.html')
    context = {
        'dati': dati,
        'nlavoratori': nlavoratori,
        'oggi': date_scadenza()['oggi'],
        'mesi1': date_scadenza()['mesi1'],
        'mesi2': date_scadenza()['mesi2'],
        'mesi6': date_scadenza()['mesi6'],
        'mesi12': date_scadenza()['mesi12'],
    }
    return HttpResponse(template.render(context, request))


def formazione(request):
    lavoratori = Formazione.objects.order_by('lavoratore')

    oggi = datetime.date.today()
    mesi1 = oggi + datetime.timedelta(days=30)
    mesi2 = oggi + datetime.timedelta(days=60)
    mesi6 = oggi + datetime.timedelta(days=366 / 2)
    mesi12 = oggi + datetime.timedelta(days=365)

    template = loader.get_template('personale/formazione.html')
    context = {
        'lavoratori': lavoratori,
        'oggi': oggi,
        'mesi1': mesi1,
        'mesi2': mesi2,
        'mesi6': mesi6,
        'mesi12': mesi12,
    }
    return HttpResponse(template.render(context, request))


def scadenza(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")


def estrai_dati(request):
    path = r'C:\Users\leonardo.masi\Documents\Personale'
    path2 = r'C:\Users\leonardo.masi\Documents\Programmi\Richiesta_Dati'
    FIN = 'elenco_ilva.csv'

    with open(os.path.join(path, FIN)) as fin:
        for row in fin:
            cognome, nome = row.split(';')
            cartella_lavoratore = '%s %s' % (cognome, nome)

            path_idoneita = os.path.join(path, cartella_lavoratore.strip())
            path_attestati = os.path.join(path, cartella_lavoratore.strip(), 'attestati')

            # idoneità
            pi = os.path.abspath(path_idoneita)
            os.chdir(pi)
            nfile = glob.glob('idon*')[0]
            da_i = os.path.join(pi, nfile)
            a_i = os.path.join(path2, '%s - %s' % (cartella_lavoratore.strip(), 'idoneità sanitaria.pdf'))

            # print(da_i, '-->', a_i)
            shutil.copy(da_i, a_i)

            # attestati
            os.chdir(path_attestati)
            nfile = glob.glob('art*')[0]
            da_i = os.path.join(path_attestati, nfile)
            a_i = os.path.join(path2, '%s - %s' % (cartella_lavoratore.strip(), 'formazione accordo stato-regione.pdf'))

            # print(da_i, '-->', a_i)
            shutil.copy(da_i, a_i)

    return HttpResponse("Dati estratti")


def leggi_contrattideterminati(request):
    path = r'C:\Users\leonardo.masi\Documents\Personale'
    FIN = r'C:\Users\leonardo.masi\Documents\Personale\CONTRATTIDETERMINATI.xlsx'
    xls = pd.ExcelFile(FIN)

    ciclo = (('CARPENT.', 'm'),
             ('RIMEC', 'r'),
             ('WELDING', 'w'),
             ('SOMMINISTRATI', 'm'))

    for foglio, azienda in ciclo:
        df = xls.parse(foglio)

        for row in df.iterrows():

            if not pd.isnull(row[0]):
                cognome = row[1][0].title().strip().replace(' ', '_').replace("o'", 'ò').replace("e’", 'è')
                nome = row[1][1].title().strip()
                qualifica = row[1][3].title().strip()
                unilav = row[1][5]

                cartella = os.path.join(path, '%s %s' % (cognome.upper(), nome))
                if not os.path.exists(cartella):
                    os.mkdir(cartella)

                # cartella2 = os.path.join(path, '%s %s' % (cognome, nome))
                # os.rename(cartella2, cartella)

                if not pd.isnull(cognome):
                    try:
                        lavoratore = Lavoratore.objects.filter(cognome=cognome.title(), nome=nome)[0]
                        res = Anagrafica.objects.get(lavoratore__id=lavoratore.id)

                        res.in_forza = True
                        res.azienda = azienda
                        res.mansione = qualifica
                        res.unilav = unilav

                        res.save()

                    except IndexError:
                        print('*** errore ----> ', cognome, nome)

    ora = datetime.datetime.now()
    return HttpResponse("""<h1 style="text-align:center">Hello, world. You're at the ''azione'' index.</h1>
                        <h2 style="text-align:center"> %s </h2>""" % ora)
