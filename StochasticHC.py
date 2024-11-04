import time
import copy
from Cube import Cube
from BaseLocalSearchAlgorithm import BaseLocalSearchAlgorithm

class StochasticHillClimbing(BaseLocalSearchAlgorithm):
    def __init__(self, cube: Cube):
        super().__init__(cube)
        self.iteration_count = 0
        self.objective_values = []
        self.time_exec = 0
        self.initial_state = 0
        self.current_score = 999999
        self.max_iterations = 10000

    def run(self):
        start_time = time.time()
        prev = time.time()
        self.cube.generate_cube()
        self.initial_state = copy.deepcopy(self.cube)
        self.current_score = self.initial_state.evaluate_objective_function()
        self.objective_values.append(self.current_score)

        while (self.iteration_count < self.max_iterations):
            self.iteration_count += 1
            successor = self.cube.generate_random_successor()
            successor_value = successor.evaluate_objective_function()

            if (successor_value < self.current_score):
                self.cube = successor
                self.current_score = successor_value
                self.objective_values.append(successor_value)
            else:
                self.objective_values.append(self.current_score)
                
            if (self.iteration_count % 10 == 0):
                print(f"Count: {self.iteration_count}")
                print(f"Current_value: {self.current_score}")
                print(f"One iteration time: {(time.time() - prev):.12f}\n\n")
                prev = time.time()

        end_time = time.time()
        self.time_exec = end_time - start_time
        print(f"Current score: {self.current_score}")
        print(f"Time execution: {self.time_exec:.8f} seconds\n\n")
        self.initial_state.display_cube()
        return {
            "initial_state": self.initial_state,
            "final_state": self.cube,
            "final_objective": self.current_score, 
            "iterations": self.iteration_count,
            "duration": self.time_exec,
            "objective_progress": self.objective_values,
        }
