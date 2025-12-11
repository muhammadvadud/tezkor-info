from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.conf import settings
import os


def generate_pdf(data: list[dict], ad_id):
    pdf_dir = os.path.join(settings.MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)

    file_path = os.path.join(pdf_dir, f"ad_users_pdf_{ad_id}.pdf")

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 30 * mm, "Ro'yxat Jadvali")

    table_data = [
        ["N", "F.I.SH", "Kompaniya nomi"]
    ]

    for i, item in enumerate(data, start=1):
        table_data.append([
            str(i),
            item.get("fish", ""),
            item.get("company", "")
        ])

    table = Table(table_data, colWidths=[15 * mm, 70 * mm, 70 * mm])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 15 * mm, height - 60 * mm - len(table_data) * 8 * mm)

    c.save()
    return file_path
