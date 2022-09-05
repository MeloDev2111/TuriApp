import numpy as np
import pandas as pd
from flask import Blueprint, current_app
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from ga.tsp import TSPViajero

viajero_bp = Blueprint('viajero_api', __name__)
api = Api(viajero_bp)


class RouteResource(Resource):
    def get(self):
        file_name = current_app.config['DISTANCE_MATRIX_FOR_TSP_FILE_NAME']
        try:
            distances = pd.read_csv(file_name)
        except FileNotFoundError:  # parent of IOError, OSError *and* WindowsError where available
            raise NotFound("not found local data: " + file_name)

        distance_matrix = np.array(distances)
        tour_size = 25

        tsp_viajero = TSPViajero()
        tsp_viajero.implementAlgorithm(distance_matrix, tour_size)

        # La distancia vuelve en metros
        # La ruta vuelve en formato array
        distancia = tsp_viajero.distance
        ruta = tsp_viajero.route

        return {
                   'route': ruta,
                   'distance': distancia
               }, 200


api.add_resource(RouteResource, '/route')
# export api_bp
