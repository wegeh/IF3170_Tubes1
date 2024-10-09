import itertools
import random
import copy

class SuccessorGenerator:
    def __init__(self, cube):
        self.cube = cube
        self.successors = []

    def generate_all_successors(self):
        indices = [(i, j, k) for i in range(self.cube.n) for j in range(self.cube.n) for k in range(self.cube.n)]
        
        # (125C2 untuk n = 5)
        index_pairs = itertools.combinations(indices, 2)
        
        for idx1, idx2 in index_pairs:
            new_cube = copy.deepcopy(self.cube)
            new_cube.swap(idx1, idx2)
            self.successors.append(new_cube)

        print(f"Generated {len(self.successors)} successor cubes.")

    def generate_random_successor(self):
        indices = [(i, j, k) for i in range(self.cube.n) for j in range(self.cube.n) for k in range(self.cube.n)]
        
        idx1, idx2 = random.sample(indices, 2)
        
        new_cube = copy.deepcopy(self.cube)
        new_cube.swap(idx1, idx2)
        
        print(f"Generated a random successor by swapping values {idx1} and {idx2}.")
        return new_cube

    def get_successors(self):
        return self.successors

# Contoh:
# from Cube import Cube
# n = 5
# magic_cube = Cube(n)
# magic_cube.generate_cube()
# magic_cube.display_cube()
# generator = SuccessorGenerator(magic_cube)
# generator.generate_all_successors()
# all_successors = generator.get_successors()
# random_successor = generator.generate_random_successor()
# random_successor.display_cube()
# random_successor.display_cube()
