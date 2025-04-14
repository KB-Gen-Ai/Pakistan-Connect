from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import qrcode
from PIL import Image
import os

def generate_pdf(data, file_path="profile.pdf"):
    """
    Create a clean PDF summary of the user profile
    """
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, f"Pakistan Connect Member Profile")
    y -= 30

    c.setFont("Helvetica", 12)
    labels = [
        "Full Name", "Email", "Phone", "City", "Country", "Job Title", "Industry",
        "Years of Experience", "Areas of Expertise", "Help Offered", "LinkedIn"
    ]

    for label, value in zip(labels, data):
        if value:
            c.drawString(50, y, f"{label}: {value}")
            y -= 20

    c.save()
    return file_path

def generate_qr_code(email, phone, linkedin=None, file_path="qr_code.png"):
    """
    Generate a QR code linking to contact info
    """
    contact_text = f"Email: {email}\nPhone: {phone}"
    if linkedin:
        contact_text += f"\nProfile: {linkedin}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(contact_text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)
    return file_path

