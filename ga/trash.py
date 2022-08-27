from tsp import TSPViajero
import json

'''
Colocar el JSON con la data en un formato adecuado
CAMPOS OBLIGATORIOS:
    1. TourSize: Cantidad de nodos
    2. DistanceMatrix: Matriz con las distancias 
    (Referencia "./data/data.json")
Si quieren partir desde la plaza es OBLIGATORIO que lo pongan nodo inicial
NO LO PONGAN COMO NODO 6 O SALDRÁ OTRO RESULTADO
'''

# Aquí va el JSON con la data que hayan obtenido de la api
data = "./data/data.json"
with open(data, "r") as tsp_data:
    tsp = json.load(tsp_data)

# Aquí empieza la lógica del algoritmo
# ↓↓↓ Este código NO LO TOQUEN ↓↓↓
tsp_viajero = TSPViajero()
tsp_viajero.implementAlgorithm(tsp)

# La distancia vuelve en kilómetros
# La ruta vuelve en formato array
distancia = tsp_viajero.distance
ruta = tsp_viajero.route

# Esto bórrenlo si quieren es para ver el resultado en consola
print(f'Ruta: {ruta}')
print(f'Distancia a recorrer: {distancia} km')
