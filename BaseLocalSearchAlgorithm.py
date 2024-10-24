import copy
from Cube import Cube

class BaseLocalSearchAlgorithm:
    def __init__(self, cube):
        self.cube = Cube
    
    def SteepestAscentHillClimbing(self):
        current_cube = copy.deepcopy(self.cube)
        current_score = current_cube.evaluate_objective_function()

        while True:
            best_successor = current_cube.get_best_successor()
            best_score = best_successor.evaluate_objective_function()

            if best_score >= current_score:
                break

            current_cube = best_successor
            current_score = best_score

        return current_cube, current_score

    def HillClimbingWithSideWayMove(self, maximum_sideways_move):
        current_cube = copy.deepcopy(self.cube)
        current_score = current_cube.evaluate_objective_function()
        sideways_moves = 0 

        while True:
            best_successor = current_cube.get_best_successor()
            best_score = best_successor.evaluate_objective_function()

            if best_score < current_score:
                current_cube = best_successor
                current_score = best_score
                sideways_moves = 0 
            elif best_score == current_score:
                sideways_moves += 1
                if sideways_moves > maximum_sideways_move:
                    break 
                current_cube = best_successor
            else:
                break 

        return current_cube, current_score


    def RandomRestartHillClimbing(self, max_restarts):
        best_cube = None
        best_score = int('inf')

        for _ in range(max_restarts):
            current_cube = copy.deepcopy(self.cube)
            current_cube.generate_cube()
            current_cube, current_score = self.SteepestAscentHillClimbing()

            if current_score < best_score:
                best_cube = current_cube
                best_score = current_score

        return best_cube, best_score

    def StochasticHillClimbing(self, max_iterations):
        current_cube = copy.deepcopy(self.cube)
        current_score = current_cube.evaluate_objective_function()

        for _ in range(max_iterations):
            random_successor = current_cube.get_random_successor()
            successor_score = random_successor.evaluate_objective_function()

            if successor_score < current_score:
                current_cube = random_successor
                current_score = successor_score

        return current_cube, current_score

    def SimulatedAnnealing(self, initial_temperature, cooling_rate):
        return

    def GeneticAlgorithm(self, population_size, max_generations):
        return