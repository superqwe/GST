import datetime
import glob
import os
import shutil
from datetime import timedelta

import pandas as pd
from django.http import HttpResponse
from django.template import loader

from personale import views_util
from personale.admin_actions import data_ultima_modifica_leggi
from personale.models import Lavoratore
from personale.views_util import date_scadenza


def index(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")


def anagrafica(request):
    lavoratori = Lavoratore.objects.all()

    nlavoratori = len(lavoratori)
    template = loader.get_template('personale/anagrafica.html')
    context = {
        'lavoratori': lavoratori,
        'nlavoratori': nlavoratori,
        'scadenza': views_util.Date_Scadenza()
    }
    return HttpResponse(template.render(context, request))


def anagrafica_per_cantiere(request):
    lavoratori = Lavoratore.objects.all()
    cantieri = Lavoratore.CANTIERE

    dati = []
    for cantiere in cantieri:
        lavoratori = Lavoratore.objects.filter(cantiere=cantiere[0])

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


def completo(request, filtro=False, ordinamento=None):
    pagina_attiva = 'in_forza' if filtro == 'in_forza' else 'tutti'
    tabella_completa = False
    nn = None

    if ordinamento == 'a':
        dati = views_util.lavoratori_suddivisi_per_azienda()
        pagina_attiva = 'azienda'
    elif ordinamento == 'c':
        dati = views_util.lavoratori_suddivisi_per_azienda('cantiere')
        pagina_attiva = 'cantiere'
    elif ordinamento == 'n':
        dati = views_util.lavoratori_con_nomine()
        pagina_attiva = 'nomine'
    elif ordinamento == 's':
        dati = views_util.lavoratori_suddivisi_per_azienda('stato')
        pagina_attiva = 'scadenza'
    elif ordinamento == 'v':
        dati = views_util.lavoratori_suddivisi_per_azienda('idoneita')
        pagina_attiva = 'idoneita'
    else:
        if filtro == 'in_forza':
            lavoratori = Lavoratore.objects.filter(in_forza=True)
        else:
            lavoratori = Lavoratore.objects.all()
            # nn = len(Anagrafica.objects.filter(in_forza=False))

        n = {'r': len(lavoratori.filter(stato='r')),
             'g': len(lavoratori.filter(stato='g')),
             'v': len(lavoratori.filter(stato='v')),
             't': len(lavoratori)}

        dati = (('Elenco Personale', lavoratori, n))
        tabella_completa = True

    template = loader.get_template('personale/principale.html')
    context = {
        'dati': dati,
        'pagina_attiva': pagina_attiva,
        'scadenza': views_util.Date_Scadenza(),
        'tabella_completa': tabella_completa,
        'data_ultima_modifica': data_ultima_modifica_leggi(),
    }
    return HttpResponse(template.render(context, request))


def formazione(request):
    lavoratori = Lavoratore.objects.all()

    oggi = datetime.date.today()
    mesi1 = oggi + datetime.timedelta(days=30)
    mesi2 = oggi + datetime.timedelta(days=60)
    mesi6 = oggi + datetime.timedelta(days=366 / 2)
    mesi12 = oggi + datetime.timedelta(days=365)

    template = loader.get_template('personale/formazione.html')
    context = {
        'lavoratori': lavoratori,
        'scadenza': views_util.Date_Scadenza()

    }
    return HttpResponse(template.render(context, request))


def scadenza(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")


def estrai_dati(request):
    path = r'C:\Users\leonardo.masi\Documents\Personale'
    path2 = r'C:\Users\leonardo.masi\Documents\Programmi\Richiesta_Dati'
    FIN = 'mario unilav.csv'

    lavoratori = Lavoratore.objects.filter(in_forza=True, azienda='m')  # , spazi_confinati__isnull=False)

    for lavoratore in lavoratori:
        cartella_lavoratore = '%s %s\\attestati' % (lavoratore.lavoratore.cognome, lavoratore.lavoratore.nome)
        path_idoneita = os.path.join(path, cartella_lavoratore)
        pi = os.path.abspath(path_idoneita)

        try:
            os.chdir(pi)
        except FileNotFoundError:
            continue

        try:
            nfile = glob.glob('spaz*')[0]
            # print('***', lavoratore, nfile)
        except IndexError:
            # print('***', lavoratore)
            continue

        da_i = os.path.join(pi, nfile)
        a_i = os.path.join(path2, '%s - %s' % (cartella_lavoratore[:-10], 'DPR177.pdf'))

        print(da_i, '-->', a_i)
        shutil.copy(da_i, a_i)
        # return HttpResponse("Dati estratti")

    with open(os.path.join(path, os.path.join(path2, FIN))) as fin:
        for row in fin:
            cognome, nome = row.split(';')
            cartella_lavoratore = '%s %s' % (cognome, nome)

            path_idoneita = os.path.join(path, cartella_lavoratore.strip())
            # path_attestati = os.path.join(path, cartella_lavoratore.strip(), 'attestati')

            # # idoneità
            # pi = os.path.abspath(path_idoneita)
            # os.chdir(pi)
            # nfile = glob.glob('idon*')[0]
            # da_i = os.path.join(pi, nfile)
            # a_i = os.path.join(path2, '%s - %s' % (cartella_lavoratore.strip(), 'idoneità sanitaria.pdf'))
            #
            # print(da_i, '-->', a_i)
            # shutil.copy(da_i, a_i)

            # unilav
            pi = os.path.abspath(path_idoneita)
            try:
                os.chdir(pi)
            except FileNotFoundError:
                # print('///', cognome, nome.strip(), 'non presente\n')
                continue

            try:
                nfile = glob.glob('uni*')[0]
            except IndexError:
                # print('***', cognome, nome)
                continue

            lavoratore = Lavoratore.objects.filter(cognome=cognome, nome=nome.strip())[0]
            if (lavoratore.in_forza):
                da_i = os.path.join(pi, nfile)
                a_i = os.path.join(path2, '%s - %s' % (cartella_lavoratore.strip(), 'unilav.pdf'))

                # print(da_i, '-->', a_i)
                # shutil.copy(da_i, a_i)
            else:
                # print('+++', cognome, nome.strip(), 'non in forza\n')
                pass

            # # attestati
            # os.chdir(path_attestati)
            # nfile = glob.glob('art*')[0]
            # da_i = os.path.join(path_attestati, nfile)
            # a_i = os.path.join(path2, '%s - %s' % (cartella_lavoratore.strip(), 'formazione accordo stato-regione.pdf'))
            #
            # # print(da_i, '-->', a_i)
            # shutil.copy(da_i, a_i)

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
                        # res = Anagrafica.objects.get(lavoratore__id=lavoratore.id)
                        #
                        # res.in_forza = True
                        # res.azienda = azienda
                        # res.mansione = qualifica
                        # res.unilav = unilav
                        #
                        # res.save()

                    except IndexError:
                        print('*** errore ----> ', cognome, nome)

    ora = datetime.datetime.now()
    return HttpResponse("""<h1 style="text-align:center">Hello, world. You're at the ''azione'' index.</h1>
                        <h2 style="text-align:center"> %s </h2>""" % ora)


def esporta_pdf(request):
    ora = datetime.datetime.now()
    return HttpResponse("""<h1 style="text-align:center">Pdf salvato</h1>
                        <h2 style="text-align:center"> %s </h2>""" % ora)


def unilav(request):
    oggi = datetime.date.today()
    mesi1 = oggi + datetime.timedelta(days=30)
    mesi2 = oggi + datetime.timedelta(days=60)
    mesi6 = oggi + datetime.timedelta(days=366 / 2)
    mesi12 = oggi + datetime.timedelta(days=365)

    fino_al = oggi + timedelta(7)
    print(fino_al)

    lavoratori = Lavoratore.objects.filter(in_forza=True, azienda='m', unilav__lte=fino_al).order_by('lavoratore')

    template = loader.get_template('personale/unilav.html')
    context = {
        'fino_al': fino_al,
        'lavoratori': lavoratori,
        'scadenza': views_util.Date_Scadenza()

    }
    return HttpResponse(template.render(context, request))


def test(request):
    lav = Lavoratore.objects.all().prefetch_related('anagrafica_set', 'formazione_set').filter(
        anagrafica__in_forza=True)

    for l in lav:
        # pp(dir(l.anagrafica_set.get().cantiere))
        print(l.anagrafica_set.get().azienda)

        # break

    ora = datetime.datetime.now()
    return HttpResponse("""<h1 style="text-align:center">test</h1>
                        <h2 style="text-align:center"> %s </h2>""" % ora)


# def azione2(request):
#     lavoratori = Lavoratore.objects.all()
#
#     for lavoratore in lavoratori:
#         anagrafica_lavoratore = Anagrafica.objects.get(lavoratore=lavoratore)
#         lavoratore.in_forza = anagrafica_lavoratore.in_forza
#         lavoratore.azienda = anagrafica_lavoratore.azienda
#         lavoratore.cantiere = anagrafica_lavoratore.cantiere
#         lavoratore.mansione = anagrafica_lavoratore.mansione
#         lavoratore.ci = anagrafica_lavoratore.ci
#         lavoratore.codice_fiscale = anagrafica_lavoratore.codice_fiscale
#         lavoratore.idoneita = anagrafica_lavoratore.idoneita
#         lavoratore.indeterminato = anagrafica_lavoratore.indeterminato
#         lavoratore.unilav = anagrafica_lavoratore.unilav
#
#         formazione_lavoratore = Formazione.objects.get(lavoratore=lavoratore)
#         lavoratore.art37 = formazione_lavoratore.art37
#         lavoratore.primo_soccorso = formazione_lavoratore.primo_soccorso
#         lavoratore.antincendio = formazione_lavoratore.antincendio
#         lavoratore.preposto = formazione_lavoratore.preposto
#         lavoratore.h2s = formazione_lavoratore.h2s
#         lavoratore.dpi3 = formazione_lavoratore.dpi3
#         lavoratore.carrello = formazione_lavoratore.carrello
#         lavoratore.ple = formazione_lavoratore.ple
#         lavoratore.gru = formazione_lavoratore.gru
#         lavoratore.imbracatore = formazione_lavoratore.imbracatore
#         lavoratore.ponteggi = formazione_lavoratore.ponteggi
#         lavoratore.lavori_quota = formazione_lavoratore.lavori_quota
#         lavoratore.spazi_confinati = formazione_lavoratore.spazi_confinati
#         lavoratore.rir = formazione_lavoratore.rir
#         lavoratore.rls = formazione_lavoratore.rls
#         lavoratore.rspp = formazione_lavoratore.rspp
#
#         nomine_lavoratore = Nomine.objects.get(lavoratore=lavoratore)
#         lavoratore.nomina_preposto = nomine_lavoratore.preposto
#         lavoratore.nomina_antincendio = nomine_lavoratore.antincendio
#         lavoratore.nomina_primo_soccorso = nomine_lavoratore.primo_soccorso
#         lavoratore.nomina_rls = nomine_lavoratore.rls
#         lavoratore.nomina_aspp = nomine_lavoratore.aspp
#
#         lavoratore.save()
#
#     ora = datetime.datetime.now()
#     return HttpResponse("""<h1 style="text-align:center">Aggiornamento DB</h1>
#                         <h2 style="text-align:center"> %s </h2>""" % ora)
