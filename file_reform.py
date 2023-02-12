from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
import textwrap
import zipfile
import csv
import io
import os


# the function to make a pdf file
def make_diploma(template, have_project, index, *args):
    # make parameters of pdf file
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    pdfmetrics.registerFont(TTFont('main', 'font.ttf'))
    pdfmetrics.registerFont(TTFont('project', 'font2.ttf'))
    can.setFont('main', 30)
    text_object = can.beginText(240, 390)
    lines = args[0].split()
    # print surname, name and father's name
    for line in lines:
        text_object.textLine(line)
    can.drawText(text_object)
    # choose scale of text of project
    if have_project:
        string = args[1]
        spl = string.split()
        for word in spl:
            if len(word) > 25 or len(textwrap.wrap(string, 25)) > 5:
                if len(word) > 30 or len(textwrap.wrap(string, 25)) > 6:
                    if len(word) > 35 or len(textwrap.wrap(string, 25)) > 7:
                        if len(word) > 38 or len(textwrap.wrap(string, 25)) > 8:
                            if len(word) > 42 or len(textwrap.wrap(string, 25)) > 9:
                                if len(word) > 47 or len(textwrap.wrap(string, 25)) > 9:
                                    if len(word) > 51 or len(textwrap.wrap(string, 25)) > 10:
                                        can.setFont('project', 9)
                                        lines = textwrap.wrap(string, 55, break_long_words=False)
                                    else:
                                        can.setFont('project', 10)
                                        lines = textwrap.wrap(string, 51, break_long_words=False)
                                else:
                                    can.setFont('project', 11)
                                    lines = textwrap.wrap(string, 47, break_long_words=False)
                            else:
                                can.setFont('project', 12)
                                lines = textwrap.wrap(string, 42, break_long_words=False)
                        else:
                            can.setFont('project', 13)
                            lines = textwrap.wrap(string, 38, break_long_words=False)
                    else:
                        can.setFont('project', 14)
                        lines = textwrap.wrap(string, 35, break_long_words=False)
                else:
                    can.setFont('project', 16)
                    lines = textwrap.wrap(string, 30, break_long_words=False)
            else:
                can.setFont('project', 20)
                lines = textwrap.wrap(string, 25, break_long_words=False)
        text_object = can.beginText(243, 200)
        # print text of project
        for line in lines:
            text_object.textLine(line)
        can.drawText(text_object)
    can.save()
    # move to the beginning of the StringIO buffer

    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    # read your existing PDF
    existing_pdf = PdfReader(open(f"templates_pdf/{template}.pdf", "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    # finally, write "output" to a real file
    output_stream = open(f"diploma_{index}.pdf", "wb")
    output.write(output_stream)
    output_stream.close()
    if index == 'special':
        with zipfile.ZipFile('diplomas.zip', mode='w'):
            pass
    with zipfile.ZipFile('diplomas.zip', mode='a') as zip_file:
        zip_file.write(f"train_out_{index}.pdf")
    os.remove(f"train_out_{index}.pdf")


# use information from csv file to making pdf files
def file_reform_from_csv():
    with open('data.csv', newline='') as csv_file:
        text = csv.reader(csv_file, delimiter="`", quotechar='|')
        with zipfile.ZipFile('diplomas.zip', mode='w'):
            pass
        for i, row in enumerate(text):
            make_diploma(row[0], int(row[1]), i, *row[2:])
