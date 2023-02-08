"""Test cases for preprocessor"""
import os
import PyPDF2
import pytest
from fpdf import FPDF


class PDFExtractor:
    """pdf extractor class"""
    def pdf_extract(self, ext_dir, source_dir, filename):
        """extracting data from POSTED pdf file"""
        self.extract_directory = ext_dir
        self.source_directory = source_dir
        self.filename = filename

        with open((os.path.join(self.source_directory, self.filename)), "rb") as pdf_file, open(
                (os.path.join(self.extract_directory, "message.txt")),
                "w",
        ) as text_file:
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            number_of_pages = read_pdf.getNumPages()

            for page_number in range(number_of_pages):
                page = read_pdf.getPage(page_number)
                page_content = page.extractText()
                text_file.write(page_content)

        text_file.close()


class TestPDFExtract:
    def test_pdf_extract(self, tmpdir):
        # setup
        ext_dir = tmpdir.mkdir("extract")
        source_dir = tmpdir.mkdir("source")
        filename = "test.pdf"
        source_file = source_dir.join(filename)

        # Generate a test PDF file
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Test PDF content", ln=1, align="C")
        pdf.output(str(source_file), "F")

        # create an instance of the class
        pdf_extractor = PDFExtractor()

        # test pdf_extract method
        pdf_extractor.pdf_extract(str(ext_dir), str(source_dir), filename)

        # verify the extracted text file
        extracted_text_file = ext_dir.join("message.txt")
        assert extracted_text_file.read() == "Test PDF content"

