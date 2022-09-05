import os

UPLOAD_FOLDER = os.path.abspath("./uploads/")
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
GOOGLE_MAPS_API_KEY = ""
DATA_COLLECTION_SERVICE_URL = "http://localhost:8000"
SCRAPED_DATA_FILE_NAME = "data.json"
DURATION_MATRIX_FILE_NAME = "matrix_duration.csv"
DISTANCE_MATRIX_FILE_NAME = "matrix_distance.csv"
DISTANCE_MATRIX_FOR_TSP_FILE_NAME ="ga/data/distances_matrix.csv"
SQLALCHEMY_DATABASE_URI = "<DBMS>://<user>:<password>@localhost:<port>/<db>"

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
    BASE_DIR = basedir


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    GOOGLE_MAPS_API_KEY = ""
    DATA_COLLECTION_SERVICE_URL = "http://localhost:8000"
    SCRAPED_DATA_FILE_NAME = "data.json"
    DURATION_MATRIX_FILE_NAME = "matrix_duration.csv"
    DISTANCE_MATRIX_FILE_NAME = "matrix_distance.csv"
    DISTANCE_MATRIX_FOR_TSP_FILE_NAME ="ga/data/distances_matrix.csv"
    SQLALCHEMY_DATABASE_URI = "<DBMS>://<user>:<password>@localhost:<port>/<db>"
