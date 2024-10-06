import unittest
import io
from unittest.mock import patch, MagicMock
from app import create_app
from app.extract import extract_text_from_pdf
# from app.analyze import analyze_recommendations

class TestFileUpload(unittest.TestCase):
    def setUp(self):
        self.app, _ = create_app('testing')
        self.client = self.app.test_client()
        self.client.testing = True 

    @patch('app.extract.extract_text_from_pdf')
    @patch('app.analyze.analyze_recommendations')
    def test_file_upload_success(self, mock_extract):
        mock_extract.return_value = "Sample extracted text"
        mock_analyze.return_value = {"recommendations": ["Sample recommendation"]}
        
        data = {
            'file': (io.BytesIO(b"fake pdf content"), 'test.pdf')
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('File processed successfully', response.get_json()['message'])
        self.assertIn('analysis', response.get_json())
        self.assertEqual(response.get_json()['analysis'], {"recommendations": ["Sample recommendation"]})

    def test_file_upload_invalid_type(self):
        data = {
            'file': (io.BytesIO(b"fake txt content"), 'test.txt')
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn('File type not allowed', response.get_json()['error'])

    def test_file_upload_empty_file(self):
        data = {
            'file': (io.BytesIO(b""), '')
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No selected file', response.get_json()['error'])

    @patch('app.extract.extract_text_from_pdf')
    def test_file_upload_extraction_error(self, mock_extract):
        mock_extract.side_effect = Exception("Extraction error")
        
        data = {
            'file': (io.BytesIO(b"fake pdf content"), 'test.pdf')
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error processing file', response.get_json()['error'])

    @patch('app.extract.extract_text_from_pdf')
    @patch('app.analyze.analyze_recommendations')
    def test_file_upload_analysis_error(self, mock_analyze, mock_extract):
        mock_extract.return_value = "Sample extracted text"
        mock_analyze.side_effect = Exception("Analysis error")
        
        data = {
            'file': (io.BytesIO(b"fake pdf content"), 'test.pdf')
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error processing file', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()