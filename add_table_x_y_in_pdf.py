import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT  # Выравнивание по левому краю



# sample_date = "12.06.2024"   
# test_start_date = "08.08.2024"


# pdf_path = r'C:/Users/user/Desktop/Новая папка/C.pdf'
# output_path = r'C:/Users/user/Desktop/Новая папка/C.pdf'

font_path = r"C:/Users/user/Desktop/Новая папка/consolas.ttf"

try:
    pdfmetrics.registerFont(TTFont("Consolas", font_path))
except Exception as e:
    print(f"Ошибка регистрации шрифта Consolas: {e}")


def add_date_info_to_pdf_to_existing_pages(pdf_path, output_path, sample_date, test_start_date, x=40, y=40, font_size=8):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        c = canvas.Canvas("temp.pdf", pagesize=letter)

        # Создаем стиль для Paragraph
        style = ParagraphStyle(
            name='DateStyle',
            fontName="Consolas",
            fontSize=font_size,
            leading=font_size * 1.28, # Межстрочный интервал (1.28 множитель)
            spaceBefore=2.6, # интервал перед абзацем
            alignment=TA_LEFT  # Выравнивание по левому краю
        )

        text_sample = f"Дата отбора пробы: {sample_date}"
        text_test = f"Дата начала испытания: {test_start_date}"

        p1 = Paragraph(text_sample, style)
        p2 = Paragraph(text_test, style)

        p1.wrapOn(c,  letter[0] - 2*x , letter[1])
        p1.drawOn(c, x, y - p1.height)
        p2.wrapOn(c, letter[0] - 2*x, letter[1])
        p2.drawOn(c, x, y - p1.height - p2.height - 2) # Добавляем 2px для дополнительного интервала


        c.save()

        temp_reader = PdfReader("temp.pdf")
        overlay = temp_reader.pages[0]
        page.merge_page(overlay)
        writer.add_page(page)

    writer.write(output_path)





add_date_info_to_pdf_to_existing_pages(pdf_path, output_path, sample_date, test_start_date, 23 * mm, 45 * mm)
print(f"PDF файл '{output_path}' создан с датами на каждой странице.")
