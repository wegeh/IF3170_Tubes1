from BaseLocalSearchAlgorithm import BaseLocalSearchAlgorithm
import time
from Cube import Cube
import copy 

class SteepestAscentHC(BaseLocalSearchAlgorithm):
    def __init__(self, cube: Cube):
        super().__init__(cube)
        self.iteration_count = 0
        self.objective_values = []
        self.time_exec = 0
    
    def run(self):
        start_time = time.time()
        prev = time.time()
        self.cube.generate_cube()
        self.initial_state = copy.deepcopy(self.cube)
        self.current_score = self.initial_state.evaluate_objective_function()
        
        
        while (True):
            self.iteration_count += 1
            successor = self.cube.get_best_successor()
        
            successor_value = successor.evaluate_objective_function()
            
            if (successor_value < self.current_score):
                self.cube = successor
                self.current_score = successor_value
                self.objective_values.append(successor_value)     
            else:
                self.objective_values.append(self.current_score)     
                end_time = time.time()
                self.time_exec = end_time-start_time
                print(self.current_score)
                print(successor_value)
                print()
                break;
            
            if self.iteration_count % 2 == 0:
                print("count", self.iteration_count)
                print("current_value", self.current_score)
                print(time.time() - prev)
                prev = time.time()
                print()
                print()
                
        # self.initial_state.display_cube()
        
        return {
            "initial_state": self.initial_state,
            "final_state": self.cube,
            "final_objective": self.current_score, 
            "iterations": self.iteration_count,
            "duration": self.time_exec,
            "objective_progress": self.objective_values,
            
        }
        
    