from BaseLocalSearchAlgorithm import BaseLocalSearchAlgorithm
import time
from Cube import Cube
import copy 

class RandomRestartHC(BaseLocalSearchAlgorithm):
    def __init__(self, cube: Cube, max_restarts: int = 100):
        super().__init__(cube)
        self.max_restarts = max_restarts
        self.iteration_count = 0
        self.total_restarts = 0
        self.objective_values = []
        self.best_score = float('inf')
        self.best_state = None
        self.time_exec = 0
    
    def run(self):
        start_time = time.time()

        for restart in range(self.max_restarts):
            self.total_restarts += 1
            self.iteration_count = 0
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
                    end_restart = time.time() - prev
                    if self.current_score < self.best_score:
                        self.best_score = self.current_score
                        self.best_state = copy.deepcopy(self.cube)
                    print("restart: ", self.total_restarts)
                    print(end_restart)
                    print(self.best_score)
                    print()
                    break;
                
                if self.iteration_count % 10 == 0:
                    print("count", self.iteration_count)
                    print("current_value", self.current_score)
                    print(time.time() - prev)
                    print()
                    print()
        
        end_time = time.time()
        self.time_exec = end_time - start_time
            
        return {
            "initial_state": self.initial_state,
            "final_state": self.best_state,
            "final_objective": self.best_score, 
            "max restart": self.max_restarts,
            "total restart": self.total_restarts,
            "duration": self.time_exec,
            "objective_progress": self.objective_values,
        }
        
if __name__ == "__main__":
    cube = Cube(5)
    max_restarts = 100

    random_restart_hc = RandomRestartHC(cube, max_restarts=max_restarts)
    results = random_restart_hc.run()
    print(results)