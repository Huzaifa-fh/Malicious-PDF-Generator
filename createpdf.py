import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random
import string
import textwrap
from PIL import Image

def generate_random_paragraphs(num_paragraphs=50):
    paragraphs = []
    for _ in range(num_paragraphs):
        words = ''.join(random.choices(string.ascii_letters + ' '*10, k=500)).split(' ')
        paragraph = ' '.join([' '.join(words[i:i+10]) for i in range(0, len(words), 10)])
        paragraphs.append(paragraph)
    return paragraphs

def generate_simple_image():
    # Generate a simple colored rectangle image
    img = Image.new('RGB', (200, 200), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    img_path = f"temp_image_{random.randint(0, 999999)}.png"
    img.save(img_path)
    return img_path

def insert_random_image(pdf, x, y):
    img_path = generate_simple_image()
    pdf.drawImage(img_path, x, y, width=200, height=200)
    os.remove(img_path)  # Clean up the image file

def create_pdf(file_path, num_pages):
    pdf = canvas.Canvas(file_path, pagesize=letter)
    paragraphs = generate_random_paragraphs(num_pages * 5)
    x, start_y = 50, 750
    y = start_y

    for paragraph in paragraphs:
        if y < 200:
            insert_random_image(pdf, 100, y - 150)
            pdf.showPage()
            y = start_y

        lines = textwrap.wrap(paragraph, width=60)
        for line in lines:
            if y < 50:
                pdf.showPage()
                y = start_y
            pdf.drawString(x, y, line)
            y -= 15
        y -= 15

    insert_random_image(pdf, 100, y - 150)
    pdf.save()

def generate_pdfs(output_directory, num_pdfs, num_pages):
    os.makedirs(output_directory, exist_ok=True)

    for i in range(1, num_pdfs + 1):
        pdf_filename = f"random_pdf_{i}.pdf"
        pdf_path = os.path.join(output_directory, pdf_filename)
        create_pdf(pdf_path, num_pages)
        print(f"Created PDF: {pdf_path}")

if __name__ == "__main__":
    num_pages = int(input("Enter the number of pages for each PDF: "))
    num_pdfs = int(input("Enter the number of PDFs to generate: "))
    output_directory = input("Enter the output directory path: ")
    generate_pdfs(output_directory, num_pdfs, num_pages)
