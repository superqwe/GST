import datetime
from pprint import pprint as pp

from django.db.models.functions import ExtractYear

from personale.models import Simulazione_Emergenza, Azienda, Lavoratore


def mesi_indietro(data, mesi):
    data -= datetime.timedelta(days=365 / 12 * mesi)
    data = datetime.date(data.year, data.month, 1)
    return data


def simulazione_emergenze(request):
    anni = Simulazione_Emergenza.objects.annotate(year=ExtractYear('data')).values_list('year')
    anni = list(set([row[0] for row in anni]))
    anni.sort(reverse=True)

    post = request.POST
    if post:
        periodo = post['periodo']

        data = None
        if periodo == 'tutto':
            simulazioni = Simulazione_Emergenza.objects.all()
        elif periodo == 'mesi12':
            oggi = datetime.datetime.today()
            data = mesi_indietro(oggi, mesi=12)
            simulazioni = Simulazione_Emergenza.objects.filter(data__gte=data)
        else:
            data = int(periodo)
            simulazioni = Simulazione_Emergenza.objects.filter(data__year=data)

        periodo = (periodo, data)
    else:
        simulazioni = Simulazione_Emergenza.objects.all()
        periodo = (None, None)

    presenze_totali = [len(Lavoratore.objects.filter(simulazione_emergenza__data=simulazione.data)) for simulazione in
                       simulazioni]

    lavoratori = Lavoratore.objects.filter(in_forza=True, azienda=Azienda.objects.get(nome='Modomec')).order_by(
        'cantiere', 'cognome')

    matrice_simulazioni = []
    stato_lavoratore = []
    presenze_per_cantiere = {}
    for lavoratore in lavoratori:
        simulazioni_lavoratore = lavoratore.simulazione_emergenza_set.all()

        rigo = [simulazione in simulazioni_lavoratore for simulazione in simulazioni]
        matrice_simulazioni.append(rigo)

        stato = any(rigo)
        stato_lavoratore.append(stato)

        if lavoratore.cantiere not in presenze_per_cantiere:
            presenze_per_cantiere[lavoratore.cantiere] = [0, 0]

        if stato:
            presenze_per_cantiere[lavoratore.cantiere][0] += 1
        else:
            presenze_per_cantiere[lavoratore.cantiere][1] += 1

    for cantiere, presenza_cantiere in presenze_per_cantiere.items():
        percentuale_presenza = 100 * presenza_cantiere[0] / sum(presenza_cantiere)
        presenze_per_cantiere[cantiere].append(percentuale_presenza)

    totali_lavoratori = stato_lavoratore.count(True), stato_lavoratore.count(False), '%.0f' % (
            stato_lavoratore.count(True) / (stato_lavoratore.count(True) + stato_lavoratore.count(False)) * 100)

    context = {'anni': anni,
               'lavoratori': lavoratori,
               'matrice_simulazioni': zip(lavoratori, matrice_simulazioni, stato_lavoratore),
               'periodo': periodo,
               'presenze_per_cantiere': presenze_per_cantiere,
               'simulazioni': zip(simulazioni, presenze_totali),
               'totali_lavoratori': totali_lavoratori,
               }

    return context
