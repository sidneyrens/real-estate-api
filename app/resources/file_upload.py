from flask import current_app, request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from ..utils.file_helpers import allowed_file
from ..extract import extract_text_from_pdf
from ..analyze import analyze_recommendations
import os

class FileUpload(Resource):
    def post(self):
        current_app.logger.debug("Received POST request for /upload")
        current_app.logger.debug(f"Request Files: {request.files}")
        current_app.logger.debug(f"Request Form: {request.form}")
        
        try:
            if 'file' not in request.files:
                current_app.logger.error("No file part in the request")
                return {'error': 'No file part'}, 400
            
            file = request.files['file']
            
            if file.filename == '':
                current_app.logger.error("No selected file")
                return {'error': 'No selected file'}, 400
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                current_app.logger.info(f"File saved successfully: {file_path}")
                
                try:
                    extracted_text = extract_text_from_pdf(file_path)
                    analysis_result = (extracted_text)
                    return {
                        'message': 'File processed successfully',
                        'filename': filename,
                        'analysis': analysis_result
                    }, 200
                except Exception as e:
                    current_app.logger.error(f"Error processing file: {str(e)}")
                    return {'error': 'Error processing file', 'details': str(e)}, 500
            else:
                current_app.logger.error("File type not allowed")
                return {'error': 'File type not allowed'}, 400
        except Exception as e:
            current_app.logger.exception("An error occurred during file upload")
            return {'error': str(e)}, 500