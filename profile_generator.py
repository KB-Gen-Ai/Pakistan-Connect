from fpdf import FPDF
import io

def generate_pdf(record):
    buffer = io.BytesIO()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"{record[1]}'s Profile", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Name: {record[1]}", ln=True)
    pdf.cell(0, 10, f"Email: {record[2]}", ln=True)
    pdf.cell(0, 10, f"Phone: {record[3]}", ln=True)
    pdf.cell(0, 10, f"Location: {record[4]}, {record[5]}", ln=True)
    pdf.cell(0, 10, f"Job Title: {record[6]}", ln=True)
    pdf.cell(0, 10, f"Industry: {record[7]}", ln=True)
    pdf.cell(0, 10, f"Experience: {record[8]} years", ln=True)
    pdf.multi_cell(0, 10, f"Expertise: {record[9]}")
    pdf.multi_cell(0, 10, f"Can Help With: {record[10]}")
    if record[11]:
        pdf.cell(0, 10, f"LinkedIn: {record[11]}", ln=True)

    pdf.output(buffer)
    buffer.seek(0)
    return buffer
