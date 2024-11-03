from BaseLocalSearchAlgorithm import BaseLocalSearchAlgorithm
import time
from Cube import Cube
import copy
import random
import numpy as np

class GeneticAlgorithm(BaseLocalSearchAlgorithm):
    def __init__(self, cube: Cube, population_size, max_iterations):
        super().__init__(cube)
        self.iteration_count = 0
        self.objective_values = []
        self.avg_objective_values = []
        self.time_exec = 0
        self.population_size = population_size
        self.max_iterations = max_iterations

    def fitness_function(self, cube):
        objective_value = cube.evaluate_objective_function()
        return (1 / (objective_value + 1e-5), objective_value)
    
    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = copy.deepcopy(self.cube)
            individual.generate_cube() 
            population.append(individual)
        return population

    def select_parents(self, population):
        fitness_values = [self.fitness_function(individu)[0] for individu in population]

        total_fitness = np.sum(fitness_values)

        selection_probabilities = [fitness / total_fitness for fitness in fitness_values]

        parents = random.choices(population, weights=selection_probabilities, k=2)
        return parents

    def order_crossover(self, parent1, parent2):
        size = 125
        start, end = sorted(random.sample(range(size), 2))

        crossover_flat = [None] * size
        parent1_flat = parent1.to_flat_list()
        parent2_flat = parent2.to_flat_list()

        crossover_flat[start:end] = parent1_flat[start:end]

        parent2_remaining = [x for x in parent2_flat if x not in crossover_flat[start:end]]
        current_index = end

        for value in parent2_remaining:
            if current_index >= size:
                current_index = 0
            while crossover_flat[current_index] is not None:
                current_index += 1
                if current_index >= size:
                    current_index = 0
            crossover_flat[current_index] = value

        crossover = Cube.from_flat_list(crossover_flat)
        return crossover

    def mutate(self, cube):
        if random.uniform(0, 1) <= 0.05: 
            flat_list = cube.to_flat_list()
            idx1, idx2 = random.sample(range(len(flat_list)), 2)
            flat_list[idx1], flat_list[idx2] = flat_list[idx2], flat_list[idx1]
            mutated_cube = Cube.from_flat_list(flat_list)
            return mutated_cube
        return cube

    def run(self):
        start_time = time.time()
        population = self.initialize_population()
        fitness_objective_values = [(individual, self.fitness_function(individual)) for individual in population]

        curr_best_individual, (curr_best_fitness, curr_best_objective) = max(fitness_objective_values, key=lambda x: x[1][0])
        self.objective_values.append(curr_best_objective)
        best_individual = curr_best_individual
        best_fitness = curr_best_fitness
        obj_val = curr_best_objective
        avg_objective_value = sum(obj_val[1] for _, obj_val in fitness_objective_values) / len(population)
        self.avg_objective_values.append(avg_objective_value)
        initial_state = copy.deepcopy(best_individual)
        

        for iteration in range(self.max_iterations):
            new_population = []
            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents(population)
                crossover = self.order_crossover(parent1, parent2)
                mutation = self.mutate(crossover)
                new_population.append(mutation)

            population = new_population

            fitness_objective_values = [(individual, self.fitness_function(individual)) for individual in population]

            curr_best_individual, (curr_best_fitness, curr_best_objective) = max(fitness_objective_values, key=lambda x: x[1][0])
            self.objective_values.append(curr_best_objective)
            best_individual = curr_best_individual
            best_fitness = curr_best_fitness
            obj_val = curr_best_objective

            avg_objective_value = sum(obj_val[1] for _, obj_val in fitness_objective_values) / len(population)
            self.avg_objective_values.append(avg_objective_value)

            if iteration % 400 == 0:  
                print(f"Iteration {iteration}: Best Objective Value = {obj_val}")

        end_time = time.time()
        self.time_exec = end_time - start_time

        return {
            "initial_state": initial_state,
            "final_state": best_individual,
            "final_objective": obj_val,
            "final_fitness": best_fitness,
            "iterations": self.max_iterations,
            "duration": self.time_exec,
            "objective_progress": self.objective_values,
            "avg_objective_progress": self.avg_objective_values
        }