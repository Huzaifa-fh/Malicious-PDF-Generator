import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random
import string
import textwrap

def generate_random_paragraphs(num_paragraphs=5):
    # Generate a number of random paragraphs for the PDF page
    paragraphs = []
    for _ in range(num_paragraphs):
        words = ''.join(random.choices(string.ascii_letters + ' '*10, k=500)).split(' ')
        paragraph = ' '.join([' '.join(words[i:i+10]) for i in range(0, len(words), 10)])
        paragraphs.append(paragraph)
    return paragraphs

def create_pdf(file_path):
    # Create a PDF with 1 page of random content
    pdf = canvas.Canvas(file_path, pagesize=letter)
    paragraphs = generate_random_paragraphs()
    x = 50
    y = 750
    for paragraph in paragraphs:
        lines = textwrap.wrap(paragraph, width=60)
        for line in lines:
            pdf.drawString(x, y, line)
            y -= 15  # move to the next line
        y -= 15  # extra space between paragraphs
    pdf.save()

def generate_pdfs(output_directory, num_pdfs):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Generate n PDFs with 1 page of random content each
    for i in range(1, num_pdfs + 1):
        pdf_filename = f"random_pdf_{i}.pdf"
        pdf_path = os.path.join(output_directory, pdf_filename)
        create_pdf(pdf_path)
        print(f"Created PDF: {pdf_path}")

if __name__ == "__main__":
    # Specify the directory where the PDFs will be created
    output_directory = "./cleanpdfs"

    # Specify the number of PDFs to generate
    num_pdfs = 10

    # Generate the PDFs
    generate_pdfs(output_directory, num_pdfs)

