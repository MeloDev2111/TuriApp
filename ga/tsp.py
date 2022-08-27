import array
import random
import numpy as np

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


class TSPViajero:
    def __init__(self):
        self.route = ""
        self.distance = 0

    def implementAlgorithm(self, tsp):
        distance_map = tsp["DistanceMatrix"]
        pop_size = tsp["TourSize"]

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register("indices", random.sample, range(pop_size), pop_size)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        def evalTSP(individual):
            distance = distance_map[individual[-1]][individual[0]]
            for gene1, gene2 in zip(individual[0:-1], individual[1:]):
                distance += distance_map[gene1][gene2]
            return distance,

        toolbox.register("mate", tools.cxPartialyMatched)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=30)
        toolbox.register("evaluate", evalTSP)

        def main():
            random.seed(169)
            pop = toolbox.population(n=300)
            hof = tools.HallOfFame(1)

            stats = tools.Statistics(lambda ind: ind.fitness.values)
            stats.register("avg", np.mean)
            stats.register("std", np.std)
            stats.register("min", np.min)
            stats.register("max", np.max)

            algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 2000, stats=stats,
                                halloffame=hof)

            return hof

        best = main()
        self.route = str(best).split('[')[2].split(']')[0].split(',')
        self.route = list(map(int, self.route))
        self.distance = evalTSP(best[0])[0]
