from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def hello(c):
    c.drawString(100, 100, 'Hello World')


def griglia(c, x, y):
    x0 = x
    y0 = y
    width = 8.5 * cm
    height = 4.5 * cm

    grigio = 0.4

    c.rect(x, y, width, height)
    c.setFillColorRGB(grigio, grigio, grigio)
    c.drawString(x + 1 * mm, y + 1 * mm, 'Datore di Lavoro:')
    c.setFillColorRGB(0, 0, 0)
    c.drawString(x + 26 * mm, y + 1 * mm, 'Domenico Montemurro'.upper())

    y += 0.5 * cm
    c.line(x, y, x + width, y)
    c.setFillColorRGB(grigio, grigio, grigio)
    c.drawString(x + 1 * mm, y + 1 * mm, 'Impresa:')
    c.setFillColorRGB(0, 0, 0)
    c.drawString(x + 14 * mm, y + 1 * mm, 'MODOMEC srl')

    y += 0.5 * cm
    c.line(x, y, x + width, y)
    c.setFillColorRGB(grigio, grigio, grigio)
    c.drawString(x + 1 * mm, y + 6 * mm, 'Data di nascita:')
    c.drawString(x + 31 * mm, y + 6 * mm, 'Data di assunzione:')

    y += 1.0 * cm
    c.line(x, y, x + width - 2.5 * cm, y)
    c.setFillColorRGB(grigio, grigio, grigio)
    c.drawString(x + 1 * mm, y + 6 * mm, 'Cognome:')
    c.drawString(x + 1 * mm, y + 1 * mm, 'Nome:')

    y += 1.0 * cm
    c.line(x, y, x + width - 2.5 * cm, y)

    c.line(x + 3.0 * cm, y0 + 1.0 * cm, x + 3.0 * cm, y0 + 2.0 * cm)
    c.line(x + 6.0 * cm, y0 + 1.0 * cm, x + 6.0 * cm, y0 + 4.5 * cm)


def scritte(c, x, y):
    pass


def genera_tesserini():
    c = canvas.Canvas('hello.pdf')

    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    c.setFont('Arial', 9)

    x = 1 * cm
    y = 20 * cm

    griglia(c, x, y)
    scritte(c, x, y)

    c.showPage()
    c.save()
