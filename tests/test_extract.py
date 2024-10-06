import unittest
import tempfile
import os
from app.extract import extract_text_from_pdf

class TestExtract(unittest.TestCase):

    def create_test_pdf(self, content):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(content)
        return temp_file.name

    def test_extract_text_from_pdf_simple(self):
        pdf_content = b"%PDF-1.7\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/Resources <<\n/Font <<\n/F1 4 0 R\n>>\n>>\n/Contents 5 0 R\n>>\nendobj\n4 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\n5 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000120 00000 n\n0000000250 00000 n\n0000000320 00000 n\ntrailer\n<<\n/Size 6\n/Root 1 0 R\n>>\nstartxref\n420\n%%EOF"
        pdf_path = self.create_test_pdf(pdf_content)

        try:
            extracted_text = extract_text_from_pdf(pdf_path)
            self.assertIn("Hello, World!", extracted_text)
        finally:
            # Clean up the temporary file
            os.unlink(pdf_path)

    def test_extract_text_from_pdf_empty(self):
        pdf_content = b"%PDF-1.7\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/Resources <<>>\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<< /Length 0 >>\nstream\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000120 00000 n\n0000000210 00000 n\ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n260\n%%EOF"
        pdf_path = self.create_test_pdf(pdf_content)

        try:
            extracted_text = extract_text_from_pdf(pdf_path)
            self.assertEqual("", extracted_text)
        finally:
            # Clean up the temporary file
            os.unlink(pdf_path)

    def test_extract_text_from_pdf_file_not_found(self):
        # Test with a non-existent file
        with self.assertRaises((FileNotFoundError, IOError)):
            extract_text_from_pdf("non_existent_file.pdf")

if __name__ == '__main__':
    unittest.main()
