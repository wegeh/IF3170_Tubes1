from BaseLocalSearchAlgorithm import BaseLocalSearchAlgorithm
import time
from Cube import Cube
import copy
import random

class GeneticAlgorithm(BaseLocalSearchAlgorithm):
    def __init__(self, cube: Cube, population_size, max_iterations):
        super().__init__(cube)
        self.iteration_count = 0
        self.objective_values = []
        self.time_exec = 0
        self.population_size = population_size
        self.max_iterations = max_iterations

    def fitness_function(self, cube):
        objective_value = cube.evaluate_objective_function()
        return 1 / (objective_value + 1e-5) 
    
    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = copy.deepcopy(self.cube)
            individual.generate_cube() 
            population.append(individual)
        return population

    def select_parents(self, population):
        total_fitness = sum(self.fitness_function(individu) for individu in population)
        selection_probabilities = [self.fitness_function(individu) / total_fitness for individu in population]
        parents = random.choices(population, weights=selection_probabilities, k=2)
        return parents

    def order_crossover(self, parent1, parent2):
        return 

    def mutate(self, cube):
        return cube

    def run(self):
        return 