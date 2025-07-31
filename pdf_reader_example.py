from PyPDF2 import PdfReader, PdfWriter

# Load the PDF
pdf_path = "/mnt/data/DAA.pdf"
reader = PdfReader(pdf_path)

# Extract text from the PDF
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

# Splitting the text based on problems
questions = text.split("Problem ")[1:]  # Remove initial header, split on problem numbers

# Generate separate PDFs for each question
pdf_paths = []
for q in questions:
    problem_number = q.split(".")[0].strip()  # Extract problem number
    output_pdf_path = f"/mnt/data/Problem_{problem_number}.pdf"

    # Create new PDF with extracted text
    writer = PdfWriter()
    writer.add_page(reader.pages[0])  # Create a new PDF page
    
    # Add extracted text to the new PDF
    from io import BytesIO
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 800, f"Problem {problem_number}")
    text_obj = c.beginText(100, 780)
    text_obj.setFont("Helvetica", 12)
    
    for line in q.split("\n"):
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.showPage()
    c.save()

    with open(output_pdf_path, "wb") as f:
        f.write(buffer.getvalue())

    pdf_paths.append(output_pdf_path)

pdf_paths
