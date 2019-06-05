import datetime
import glob
import os
import shutil
from datetime import timedelta

import openpyxl
import pandas as pd
from django.db.models import Count
from django.http import HttpResponse
from django.template import loader
from django_pandas.io import read_frame
from openpyxl.styles import Side, Border, PatternFill, Font, Alignment

from personale import views_util, views_estrai_dati
from personale.admin_actions import data_ultima_modifica_leggi
from personale.models import Lavoratore, Azienda
from personale.views_util import autorizzato


def index(request):
    return HttpResponse("Hello, world. You're at the ''personale'' index.")


def completo(request, filtro=False, ordinamento=None):
    pagina_attiva = 'in_forza' if filtro == 'in_forza' else 'tutti'
    tabella_completa = False

    if ordinamento == 'a':
        dati = views_util.lavoratori_suddivisi_per_azienda()
        pagina_attiva = 'azienda'
    elif ordinamento == 'am':
        dati = views_util.lavoratori_suddivisi_per_azienda('arcelormittal')
        pagina_attiva = 'arcelormittal'
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
        dati = views_util.lavoratori_suddivisi_per_azienda(in_forza=False)
        pagina_attiva = 'tutti'

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
                                           unilav__lte=fino_al, unilav__gte=oggi)
    lavoratori_r = Lavoratore.objects.filter(in_forza=True, azienda=Azienda.objects.get(nome='Modomec'),
                                             unilav__lt=oggi)

    n = {'r': len(lavoratori_r), 'g': len(lavoratori)}
    n['t'] = n['g'] + n['r']

    template = loader.get_template('personale/unilav.html')
    context = {
        'autorizzato': autorizzato(request.user),
        'fino_al': fino_al,
        'lavoratori': lavoratori,
        'lavoratori_r': lavoratori_r,
        'scadenza': views_util.Date_Scadenza(),
        'n': n
    }

    return HttpResponse(template.render(context, request))


def mansioni(request):
    mansioni = Lavoratore.objects.filter(azienda=Azienda.objects.get(nome='Modomec')).values('mansione').annotate(
        totale=Count('mansione')).order_by('-totale')

    dati = []
    for mansione in mansioni:
        dati.append((mansione['totale'], mansione['mansione']))
        print('%2i' % mansione['totale'], mansione['mansione'])

    dati = pd.DataFrame(dati, columns=('n', 'mansione'))
    dati.to_excel('mansioni.xlsx', sheet_name='mansioni')

    ora = datetime.datetime.now()
    return HttpResponse("""<h1 style="text-align:center">mansioni.xlsx creato</h1>
                        <h2 style="text-align:center"> %s </h2>""" % ora)


def test(request):
    mansioni = Lavoratore.objects.filter(azienda=Azienda.objects.get(nome='Modomec')).values('mansione').annotate(
        totale=Count('mansione')).order_by('-totale')

    for mansione in mansioni:
        print('%2i' % mansione['totale'], mansione['mansione'])

    ora = datetime.datetime.now()
    return HttpResponse("""<h1 style="text-align:center">test</h1>
                        <h2 style="text-align:center"> %s </h2>""" % ora)

def estrai_dati(request):
    views_estrai_dati.estrai_cfg()
    template = loader.get_template('personale/principale.html')
    context = {
        'autorizzato': autorizzato(request.user),
        'estrai_dati': True,
        'data_ultima_modifica': data_ultima_modifica_leggi(),
    }
    return HttpResponse(template.render(context, request))


def estrai_dati2(request):
    ora = datetime.datetime.now()
    errore = views_estrai_dati.estrai_principale(request)
    print(errore)

    if errore:
        return HttpResponse("""<h1 style="text-align:center">dati estratti</h1>
                                <h2 style="text-align:center">%s</h2> 
                                <p style="text-align:center">%s</p>""" % (ora, errore))

    return HttpResponse("""<h1 style="text-align:center">dati estratti</h1>
                        <h2 style="text-align:center"> %s </h2>""" % ora)


def formazione(request):
    ora = datetime.datetime.now()
    modomec = Lavoratore.objects.filter(azienda__nome='Modomec', in_forza=True).order_by('cognome', 'nome')
    building = Lavoratore.objects.filter(azienda__nome='Building', in_forza=True).order_by('cognome', 'nome')
    rimec = Lavoratore.objects.filter(azienda__nome='Rimec', in_forza=True).order_by('cognome', 'nome')
    welding = Lavoratore.objects.filter(azienda__nome='Welding', in_forza=True).order_by('cognome', 'nome')

    lavoratori = (modomec, building, rimec, welding)
    aziende = ('modomec', 'building', 'rimec', 'welding')

    with pd.ExcelWriter('formazione.xlsx', engine='openpyxl') as writer:
        for lav, azienda in zip(lavoratori, aziende):
            dati = read_frame(lav)
            dati.drop(
                ['id', 'in_forza', 'azienda', 'ci', 'codice_fiscale', 'idoneita', 'indeterminato', 'unilav', 'rls',
                 'stato', 'rspp', 'nomina_preposto', 'nomina_antincendio', 'nomina_primo_soccorso', 'nomina_rls',
                 'nomina_aspp'],
                axis=1, inplace=True)
            dati.to_excel(writer, azienda)

        writer.save()

    wb = openpyxl.load_workbook('formazione.xlsx')

    for azienda in aziende:
        ws = wb[azienda]

        ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
        ws.page_setup.paperSize = ws.PAPERSIZE_A3

        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToHeight = False

        ws.print_title_rows = '1:2'
        ws.oddFooter.right.text = "Page &[Page] of &N"
        ws.oddFooter.left.text = "Aggiornato al %s " % datetime.datetime.now().strftime("%d/%m/%y")

        ws.delete_cols(1, 1)
        ws.insert_rows(1)
        ws.cell(row=1, column=1).value = azienda.upper()
        ws['A1'].font = Font(size=18, color='007e60')

        for cell in ws['A2:S2'][0]:
            cell.border = Border(top=Side(border_style='thin', color='000000'),
                                 bottom=Side(border_style='thin', color='000000'))

        max_row = ws.max_row
        rows = ws['A3:S%i' % max_row]
        for i, row in enumerate(rows):

            for cell in row:
                cell.border = Border(bottom=Side(border_style='thin', color='cccccc'))
                cell.number_format = 'DD/MM/YY'

                if cell.column >= 'E':
                    cell.alignment = Alignment(horizontal='center')

                if i % 2:
                    cell.fill = PatternFill(start_color='eeeeee', end_color='eeeeee', fill_type='solid')

        for cell in ws['A%i:S%i' % (max_row, max_row)][0]:
            print(cell.column)
            cell.border = Border(bottom=Side(border_style='thin', color='000000'), )

        dims = {}
        for row in ws.rows:
            for cell in row:
                if cell.value:
                    dims[cell.column] = max((dims.get(cell.column, 0), len(str(cell.value))))
        for col, value in dims.items():
            ws.column_dimensions[col].width = value

        wb.save('formazione.xlsx')

    wb.close()

    if os.path.exists('formazione.xlsx'):
        with open('formazione.xlsx', "rb") as excel:
            data = excel.read()

        response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s_Report.xlsx' % id
        return response

    return HttpResponse("""<h1 style="text-align:center">formazione</h1>
                        <h2 style="text-align:center"> %s </h2>""" % ora)
