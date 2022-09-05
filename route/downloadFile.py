from flask import Blueprint, send_from_directory

from config import UPLOAD_FOLDER

downloadRoute = Blueprint('downloadRoute', __name__)

@downloadRoute.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)
