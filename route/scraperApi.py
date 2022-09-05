import requests
from flask import Blueprint, current_app
from flask_restful import Api, Resource
from werkzeug.exceptions import BadGateway

scraper_bp = Blueprint('scraper_api', __name__)
api = Api(scraper_bp)


class Data(Resource):

    def get(self):
        file_name = current_app.config['SCRAPED_DATA_FILE_NAME']
        try:
            with open(current_app.config['UPLOAD_FOLDER'] + "/" + file_name, encoding="mbcs") as file:
                return {'message': "data already scraped"}, 409
        except FileNotFoundError:  # parent of IOError, OSError *and* WindowsError where available
            pass

        #todo: upgrade Web Scraping service a una api rest en node para poder realizar el envio de archivos facilmente
        response = requests.get(url=current_app.config['DATA_COLLECTION_SERVICE_URL'] + "/index.html")

        if not response["status_code"] == 200:
            raise BadGateway("external service error: Web Scraping service fail")

        return {'message': "scraping data"}, 200


api.add_resource(Data, '/scrape')
# export api_bp
