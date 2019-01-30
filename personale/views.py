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
from personale.models import Lavoratore, Azienda

from pprint import pprint as pp

from personale.views_util import autorizzato


def index(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")


def completo(request, filtro=False, ordinamento=None):
    pagina_attiva = 'in_forza' if filtro == 'in_forza' else 'tutti'
    tabella_completa = False

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

    template = loader.get_template('personale/principale.html')
    context = {
        'autorizzato': autorizzato(request.user),
        'dati': dati,
        'pagina_attiva': pagina_attiva,
        'scadenza': views_util.Date_Scadenza(),
        'tabella_completa': tabella_completa,
        'data_ultima_modifica': data_ultima_modifica_leggi(),
    }
    return HttpResponse(template.render(context, request))


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


def unilav(request):
    oggi = datetime.date.today()
    fino_al = oggi + timedelta(7)

    lavoratori = Lavoratore.objects.filter(in_forza=True, azienda=Azienda.objects.get(nome='Modomec'),
                                           unilav__lte=fino_al)
    lavoratori_r = Lavoratore.objects.filter(in_forza=True, azienda=Azienda.objects.get(nome='Modomec'),
                                             unilav__lt=oggi)

    n = {'r': len(lavoratori_r), 't': len(lavoratori)}
    n['g'] = n['t'] - n['r']

    template = loader.get_template('personale/unilav.html')
    context = {
        'autorizzato': autorizzato(request.user),
        'fino_al': fino_al,
        'lavoratori': lavoratori,
        'scadenza': views_util.Date_Scadenza(),
        'n': n
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


def estrai_dati2(request):
    def copia(path_da, nome_pdf, cognome, nome, nome_documento):
        da = os.path.join(path_da, nome_pdf)
        a = os.path.join(path2, '%s %s - %s.pdf' % (cognome, nome, nome_documento))
        # print(da, '-->', a)
        print('  ', nome_documento)
        shutil.copy(da, a)

    class Estrai:
        unilav = 1
        idoneita = 1

        # formazione
        art37 = 1
        preposto = 1
        primo_soccorso = 1
        antincendio = 1
        h2s = 1
        dpi3 = 1
        muletto = 1
        ple = 1
        gru = 1
        imbracatore = 1
        spazi_confinati = 1
        ponteggi = 1
        rir = 1

        # nomine
        nomina_preposto = 1
        nomina_primo_soccorso = 1
        nomina_antincendio = 1

        def formazione(self):
            attestati = ('art37' * self.art37, 'preposto' * self.preposto, 'primo.soccorso' * self.primo_soccorso,
                         'antincendio' * self.antincendio, 'h2s' * self.h2s, 'dpi3' * self.dpi3,
                         'carrelli' * self.muletto, 'ple' * self.ple, 'autogru' * self.gru,
                         'imbracatore' * self.imbracatore, 'spazi.confinati' * self.spazi_confinati,
                         'ponteggi' * self.ponteggi, 'rir' * self.rir)
            return attestati

        def nomine(self):
            incarico = ('nomina.preposto' * self.nomina_preposto, 'nomina.primo.soccorso' * self.nomina_primo_soccorso,
                        'nomina.antincendio' * self.nomina_antincendio)
            return incarico
    path_home = os.getcwd()
    path = r'C:\Users\leonardo.masi\Documents\Personale'
    path2 = r'C:\Users\leonardo.masi\Documents\Programmi\Richiesta_Dati'
    FIN = '190129 AC Boiler.xlsx'

    xls = pd.ExcelFile(os.path.join(path2, FIN))
    df = xls.parse('1d')

    for row in df.iterrows():
        cognome = row[1]['Cognome']
        nome = row[1]['Nome']
        # lavoratore = Lavoratore.objects.get(cognome=cognome, nome=nome)

        print(cognome, nome)

        path_lavoratore = os.path.join(path, "%s %s" % (cognome, nome))
        path_attestati = os.path.join(path, "%s %s" % (cognome, nome), 'attestati')
        path_nomine = os.path.join(path, "%s %s" % (cognome, nome), 'nomine')

        # documenti base
        os.chdir(path_lavoratore)

        if Estrai.unilav:
            unilav = glob.glob('unilav*.pdf')

            if unilav:
                copia(path_lavoratore, unilav[0], cognome, nome, 'unilav')

        if Estrai.idoneita:
            idoneita = glob.glob('idoneit*.pdf')

            if idoneita:
                copia(path_lavoratore, idoneita[0], cognome, nome, 'idoneità')

        # attestati corsi formazione
        if os.path.isdir(path_attestati):
            os.chdir(path_attestati)

            for corso in Estrai.formazione(Estrai):
                certificato = glob.glob('%s*.pdf' % corso)
                if certificato:
                    copia(path_attestati, certificato[0], cognome, nome, corso)

        # lettere incarico
        if os.path.isdir(path_nomine):
            os.chdir(path_nomine)

            for nomina in Estrai.nomine(Estrai):
                incarico = glob.glob('%s*.pdf' % nomina)

                if incarico:
                    copia(path_nomine, incarico[0], cognome, nome, nomina)

    os.chdir(path_home)
    ora = datetime.datetime.now()
    return HttpResponse("""<h1 style="text-align:center">dati estratti</h1>
                        <h2 style="text-align:center"> %s </h2>""" % ora)
