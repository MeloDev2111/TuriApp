import json

from flask import Blueprint, current_app
from flask_restful import Api, Resource
from werkzeug.exceptions import BadGateway
from models.Location import Location
import googlemaps
import numpy as np
import pandas as pd

from route.LocationApi import locations_schema

maps_bp = Blueprint('maps_api', __name__)
api = Api(maps_bp)


def map_to_distance_matrix(response_google_maps_api: dict, index_origin: int) -> list:
    distance = None
    duration = None
    touristic_locations = response_google_maps_api["origin_addresses"]
    distance_duration_matrix = [[] for __ in touristic_locations]
    row_index = 1
    for row in response_google_maps_api["rows"]:
        print(row)
        for column in row["elements"]:
            if column.get("distance", None):
                distance = column["distance"]["value"]
            if index_origin != row_index:
                distance_duration_matrix[0].append(f"{index_origin},{row_index}, {distance}")
            row_index += 1
    return distance_duration_matrix


def map_to_duration_matrix(response_google_maps_api: dict, index_origin: int) -> list:
    distance = None
    duration = None
    touristic_locations = response_google_maps_api["origin_addresses"]
    distance_duration_matrix = [[] for __ in touristic_locations]
    row_index = 1
    for row in response_google_maps_api["rows"]:
        print(row)
        for column in row["elements"]:
            if column.get("duration", None):
                duration = column["duration"]["value"]
            if index_origin != row_index:
                distance_duration_matrix[0].append(f"{index_origin},{row_index}, {duration}")
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
        #return {'message': "generating matrix"}, 200

        # --------------------------------------------------------------------------------------------------------------

        gmaps = googlemaps.Client(key=current_app.config['GOOGLE_MAPS_API_KEY'])

        # return valid keys for the google maps api

        # todo: get touristic locations formatted {"lat" : -33.867486, "lng" : 151.206990} <- Arreglo de este objeto
        # get from DB

        locations = Location.query.all()
        dataInJson = locations_schema.dump(locations)

        touristic_locations = []
        for location in dataInJson:
            touristic_locations.append(str(location['lat']) + "," + str(location['lng']))

        all_results_distance = []
        all_results_duration = []

        origin_index = 1

        for origin in touristic_locations:
            my_dist = gmaps.distance_matrix(
                origins=[origin],
                destinations=touristic_locations,
                mode="driving",
                language="es-419",
                transit_mode="bus"
            )
            data_distance = map_to_distance_matrix(my_dist, origin_index)

            data_duration = map_to_duration_matrix(my_dist, origin_index)

            for row in data_distance[0]:
                all_results_distance.append(row)
            for row in data_duration[0]:
                all_results_duration.append(row)

            origin_index += 1

        arr = np.asarray(all_results_distance)
        df = pd.DataFrame(arr)
        df.to_csv(current_app.config['UPLOAD_FOLDER'] + "/" + current_app.config['DISTANCE_MATRIX_FILE_NAME'], header=False, index=False)

        arr = np.asarray(all_results_duration)
        df = pd.DataFrame(arr)
        df.to_csv(current_app.config['UPLOAD_FOLDER'] + "/" + current_app.config['DURATION_MATRIX_FILE_NAME'], header=False, index=False)

        return {}, 201

    # ----------------------------------------------------------------------------------------------------------------------

    def delete(self):
        # todo: Elimina los archivos csv de matrix de distancia y matrix de duracion
        return {}, 204


api.add_resource(MatrixDistanceDuration, '/generate_matrices')
# export api_bp

