from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from .config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    api = Api(app)

    from .resources.file_upload import FileUpload
    api.add_resource(FileUpload, '/upload')

    return app, api
