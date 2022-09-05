import json
import os

from flask import current_app
from flask import request, Blueprint
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound, BadRequest
from werkzeug.utils import secure_filename

from infrastructure.database import db_session
from models.Location import Location

ALLOWED_EXTENSIONS = {"json", "csv"}

files_bp = Blueprint('files_api', __name__)
api = Api(files_bp)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class Files(Resource):

    def get(self, file_name):
        try:
            with open(current_app.config['UPLOAD_FOLDER'] + "/" + file_name, encoding="mbcs") as file:
                data = json.loads(file.read())
                return {'local_data': data}
        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            raise NotFound("not found local data: " + file_name)

    def post(self):
        # check if the post request has the file part
        if 'file' not in request.files:
            raise BadRequest("No file part")

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            raise BadRequest("No selected file")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_save = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(path_save)
            # todo: arreglar que se devuelva la url de descarga bien
            # return {'download_url': "" + url_for('download_file', name=filename)}, 201
        else:
            raise BadRequest("Not allowed file extension")

        # todo: agregar el guardado en bd

        # read file and save in db
        file_json = open(path_save, encoding="mbcs")
        data = json.loads(file_json.read())

        # recorrer el json y guardarlo en la bd
        for item in data:
            location = Location(name=item['nombre'], lat=item['longitud'], lng=item['latitud'])
            db_session.add(location)
            db_session.commit()
        return {'message': "All locations has been saved"}, 201


api.add_resource(Files, '/files/<string:file_name>', '/files')
# export api_bp
