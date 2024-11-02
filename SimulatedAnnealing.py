from BaseLocalSearchAlgorithm import BaseLocalSearchAlgorithm
import time
from Cube import Cube
import copy 
import math
import random

class SimulatedAnnealing(BaseLocalSearchAlgorithm):
    def __init__(self, cube: Cube, initial_temperature):
        super().__init__(cube)
        self.iteration_count = 0
        self.objective_values = []
        self.time_exec = 0
        self.temperature = initial_temperature
        self.cooling_rate = 0.995
        self.probability_values = []
        self.stuck_frequency = 0

    def run(self):
        start_time = time.time()
        prev_time = time.time()
        self.cube.generate_cube()
        self.initial_state = copy.deepcopy(self.cube)
        self.current_score = self.initial_state.evaluate_objective_function()

        while self.temperature > 1:
            self.iteration_count += 1
            successor = self.cube.get_random_successor()
            successor_value = successor.evaluate_objective_function()

            delta_e = successor_value - self.current_score

            if delta_e < 0:
                self.cube = successor
                self.current_score = successor_value
                self.objective_values.append(successor_value)
            else:
                probability = math.exp(-delta_e / self.temperature)
                self.probability_values.append(probability)
                if random.uniform(0, 1) < probability:
                    self.cube = successor
                    self.current_score = successor_value
                    self.objective_values.append(successor_value)
                else:
                    self.stuck_frequency += 1

            self.temperature *= (self.cooling_rate ** self.iteration_count)

            if self.iteration_count % 1 == 0:
                print("Iteration count:", self.iteration_count)
                print("Current objective value:", self.current_score)
                print("Temperature:", self.temperature)
                print(time.time() - prev_time)

        end_time = time.time()
        self.time_exec = end_time - start_time
        print(self.current_score)
        print(successor_value)
        print()

        return {
            "initial_state": self.initial_state,
            "final_state": self.cube,
            "final_objective": self.current_score,
            "iterations": self.iteration_count,
            "duration": self.time_exec,
            "objective_progress": self.objective_values,
            "probability_progress": self.probability_values,
            "final_temperature": self.temperature,
            "stuck_frequency": self.stuck_frequency / self.iteration_count
        }
    