from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from infrastructure.ma import ma

app = Flask(__name__)
CORS(app, resources=[r"/files/*"], origins="http://localhost:8000")

app.config.from_object("config.DevelopmentConfig")

with app.app_context():
    from infrastructure.database import init_db
    init_db()

ma.init_app(app)

# import routes
from route.filesApi import files_bp
from route.downloadFile import downloadRoute
from route.scraperApi import scraper_bp
from route.LocationApi import location_bp, deleteAllLocationsRoute
from route.googleMapsApi import maps_bp


app.register_blueprint(scraper_bp)
app.register_blueprint(files_bp)
app.register_blueprint(downloadRoute)
app.register_blueprint(location_bp)
app.register_blueprint(deleteAllLocationsRoute)
app.register_blueprint(maps_bp)

api = Api(app)
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

# <------------- RUN --------------->
if __name__ == "__main__":
    app.run(debug=True)
