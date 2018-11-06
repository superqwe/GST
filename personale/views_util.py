import datetime


def date_scadenza():
    oggi = datetime.date.today()
    mesi1 = oggi + datetime.timedelta(days=30)
    mesi2 = oggi + datetime.timedelta(days=60)
    mesi6 = oggi + datetime.timedelta(days=366 / 2)
    mesi12 = oggi + datetime.timedelta(days=365)

    return {'oggi': oggi,
            'mesi1': mesi1,
            'mesi2': mesi2,
            'mesi6': mesi6,
            'mesi12': mesi12
            }
