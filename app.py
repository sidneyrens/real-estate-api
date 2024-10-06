from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import sys
import logging
import unittest

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
api = Api(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class FileUpload(Resource):
    def post(self):
        app.logger.debug("Received POST request for /upload")
        app.logger.debug(f"Request Files: {request.files}")
        app.logger.debug(f"Request Form: {request.form}")
        
        try:
            if 'file' not in request.files:
                app.logger.error("No file part in the request")
                return {'error': 'No file part'}, 400
            
            file = request.files['file']
            
            if file.filename == '':
                app.logger.error("No selected file")
                return {'error': 'No selected file'}, 400
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                app.logger.info(f"File saved successfully: {file_path}")
                return {'message': 'File uploaded successfully', 'filename': filename}, 200
            else:
                app.logger.error("File type not allowed")
                return {'error': 'File type not allowed'}, 400
        except Exception as e:
            app.logger.exception("An error occurred during file upload")
            return {'error': str(e)}, 500

api.add_resource(FileUpload, '/upload')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover('tests', pattern='test_*.py')
        test_runner = unittest.TextTestRunner(verbosity=2)
        test_runner.run(test_suite)
    else:
        app.run(debug=True, host='localhost', port=5001)