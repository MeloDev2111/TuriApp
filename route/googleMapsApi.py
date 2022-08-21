from flask import Blueprint, current_app
from flask_restful import Api, Resource
from werkzeug.exceptions import BadGateway
from models.Location import Location
import googlemaps
import numpy as np

maps_bp = Blueprint('maps_api', __name__)
api = Api(maps_bp)


def map_to_distance_duration_matrix(response_google_maps_api: dict) -> list:
    distance = None
    duration = None
    touristic_locations = response_google_maps_api["origin_addresses"]
    distance_duration_matrix = [[] for __ in touristic_locations]

    row_index = 0
    for row in response_google_maps_api["rows"]:
        for column in row["elements"]:
            if column.get("distance", None):
                distance = column["distance"]["value"]
            if column.get("duration", None):
                duration = column["duration"]["value"]
            distance_duration_matrix[row_index].append({
                "distance": distance,
                "duration": duration
            })
        row_index += 1
    return distance_duration_matrix


class MatrixDistanceDuration(Resource):

# ----------------------------------------------------------------------------------------------------------------------

    def get(self):
        duration_matrix_file_name = current_app.config['DURATION_MATRIX_FILE_NAME']
        distance_matrix_file_name = current_app.config['DISTANCE_MATRIX_FILE_NAME']
        try:
            with open(current_app.config['UPLOAD_FOLDER'] + "/" + duration_matrix_file_name, encoding="mbcs") as file1:
                return {'message': "duration matrix already generated"}, 409
        except FileNotFoundError:
            pass

        try:
            with open(current_app.config['UPLOAD_FOLDER'] + "/" + distance_matrix_file_name, encoding="mbcs") as file2:
                return {'message': "distance matrix already generated"}, 409
        except FileNotFoundError:
            pass

        #todo: for testing -- BORRAR
        return {'message': "generating matrix"}, 200

        # --------------------------------------------------------------------------------------------------------------

        gmaps = googlemaps.Client(key=current_app.config['GOOGLE_MAPS_API_KEY'])
        # todo: get touristic locations formatted {"lat" : -33.867486, "lng" : 151.206990} <- Arreglo de este objeto
        # get from DB
        locations = Location.query.all() # tal vez un for each y le aplicas coordinates()
        dataInJson = locations_schema.dump(locations)

        # todo: testear las lineas de arriba

        touristic_locations = []

        # todo: new request with location and latitude
        my_dist = gmaps.distance_matrix(
            origins=touristic_locations,
            destinations=touristic_locations,
            # mode="driving",
            # language="es-419",
            # transit_mode="bus"
            # look for the needed parameters in the api
        )

        if not my_dist.get("status") == "OK":
            raise BadGateway("external service error: Google Maps API fetch fail")
        else:
            matrix = map_to_distance_duration_matrix(my_dist)
            # todo separe into 2 csv, uno con distancias y otro con duracion
            distance_matrix = []
            duration_matrix = []
            np.savetxt(current_app.config['UPLOAD_FOLDER'] + "/" + current_app.config['DISTANCE_MATRIX_FILE_NAME'],
                       distance_matrix,
                       delimiter=", ",
                       fmt='% s')

            np.savetxt(current_app.config['UPLOAD_FOLDER'] + "/" + current_app.config['DURATION_MATRIX_FILE_NAME'],
                       duration_matrix,
                       delimiter=", ",
                       fmt='% s')
            return {}, 201

# ----------------------------------------------------------------------------------------------------------------------

    def delete(self):
        # todo: Elimina los archivos csv de matrix de distancia y matrix de duracion
        return {}, 204


api.add_resource(MatrixDistanceDuration, '/generate_matrices')
# export api_bp

