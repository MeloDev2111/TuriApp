import pandas as pd

from tsp import TSPViajero
import numpy as np

distances = pd.read_csv("./data/distances_matrix.csv")
distance_matrix = np.array(distances)
tour_size = 25

tsp_viajero = TSPViajero()
tsp_viajero.implementAlgorithm(distance_matrix, tour_size)

# La distancia vuelve en metros
# La ruta vuelve en formato array
distancia = tsp_viajero.distance
ruta = tsp_viajero.route

# Esto bórrenlo si quieren es para ver el resultado en consola
print(f'Ruta: {ruta}')
print(f'Distancia a recorrer: {distancia} metros')
