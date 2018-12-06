import glob
import os
import re

MANSIONI = (
    'addetto alle pulizie',
    "apprendista addetto al controllo qualita'",
    'aiuto tubista',
    'aiuto ponteggiatore',
    'autista',
    'autista/gruista',
    'carpentiere in ferro',
    'carpentiere tubista',
    'centralinista',
    'conduttore di macchine a controllo numerico',
    'elettricista',
    'impiegato tecnico - capo squadra',
    'impiegato tecnico',
    'impiegato di concetto',
    'operatore macchine utensili',
    'ponteggiatore',
    'preventivista',
    'tubista montatore',
    'tubista navale',
    'tubista',
    'sabbiatore',
    'saldatore',
)


def analizza(unilav):
    unilav = unilav.replace('pdf', 'txt')
    mansioni = r'(%s)' % r'\n)|('.join(MANSIONI)
    regrex = re.compile(mansioni)

    with open(unilav, 'r') as fin:
        dati = fin.read().lower()

        res = regrex.search(dati)

        if res:
            print(res.group().strip())


def main():
    exe = os.path.join(os.getcwd(), 'pdftotext.exe')
    base_path_doc = r'C:\Users\leonardo.masi\Documents\Personale'

    for root, dirs, files in os.walk(base_path_doc):
        cartella = os.path.split(root)[-1].lower()

        if not cartella in ('attestati', 'scaduti', 'nomine', 'cantiere'):

            os.chdir(root)
            pdf = glob.glob('unilav*.pdf')

            if pdf:
                unilav = pdf[0]
                cmd = '%s "%s"' % (exe, unilav)
                print(root)
                os.popen(cmd)

                analizza(unilav)

                print()


if __name__ == '__main__':
    main()
