import numpy as np
import random
import itertools
import copy

class Cube:
    def __init__(self, n):
        self.size = n
        self.magic_number = n * (n**3 + 1) // 2
        self.cube = np.zeros((n, n, n), dtype=int)

    def generate_cube(self):
        numbers = np.arange(1, self.size ** 3 + 1)
        np.random.shuffle(numbers)
        self.cube = numbers.reshape((self.size, self.size, self.size))

    def display_cube(self):
        # Print per layer baru print per baris
        for layer in self.cube:
            print(layer)
            print() 

    def swap(self, idx1, idx2):
        # i = layer, j = baris, k = kolom
        i1, j1, k1 = idx1
        i2, j2, k2 = idx2
    
        self.cube[i1, j1, k1], self.cube[i2, j2, k2] = self.cube[i2, j2, k2], self.cube[i1, j1, k1]

    def evaluate_objective_function(self):
        n = self.size
        magic_number = self.magic_number

        # Menggunakan NumPy untuk menghitung total selisih lebih efisien
        row_sums = np.sum(self.cube, axis=2)  
        col_sums = np.sum(self.cube, axis=1)  
        pillar_sums = np.sum(self.cube, axis=0) 

        # Total perbedaan untuk baris, kolom, dan tiang
        total_diff = np.sum(np.abs(row_sums - magic_number))
        total_diff += np.sum(np.abs(col_sums - magic_number))
        total_diff += np.sum(np.abs(pillar_sums - magic_number))

        # Diagonal 3D pada cube 
        main_diag_1 = np.trace(self.cube, axis1=0, axis2=1)
        main_diag_2 = np.trace(np.flip(self.cube, axis=2), axis1=0, axis2=1)
        main_diag_3 = np.trace(np.flip(self.cube, axis=1), axis1=0, axis2=2)
        main_diag_4 = np.trace(np.flip(self.cube, axis=0), axis1=1, axis2=2)

        total_diff += np.abs(main_diag_1 - magic_number)
        total_diff += np.abs(main_diag_2 - magic_number)
        total_diff += np.abs(main_diag_3 - magic_number)
        total_diff += np.abs(main_diag_4 - magic_number)

        # Diagonal per layer (bidang horizontal)
        for i in range(n):
            plane_diag_1 = np.sum(self.cube[i, np.arange(n), np.arange(n)])
            plane_diag_2 = np.sum(self.cube[i, np.arange(n), np.arange(n - 1, -1, -1)])
            total_diff += np.abs(plane_diag_1 - magic_number)
            total_diff += np.abs(plane_diag_2 - magic_number)

        self.current_objective_value = total_diff
        return total_diff

    def generate_all_successors(self):
        
        indices = [(i, j, k) for i in range(self.size) for j in range(self.size) for k in range(self.size)]
        index_pairs = itertools.combinations(indices, 2)  

        for idx1, idx2 in index_pairs:
            self.swap(idx1, idx2)
            yield self  
            self.swap(idx1, idx2)

    def generate_random_successor(self):
        
        indices = [(i, j, k) for i in range(self.size) for j in range(self.size) for k in range(self.size)]
        idx1, idx2 = random.sample(indices, 2)

        self.swap(idx1, idx2)
        successor = copy.deepcopy(self) 
        self.swap(idx1, idx2)

        return successor

    def get_best_successor(self):
        
        best_cube = None
        best_score = float('inf')

        for successor in self.generate_all_successors():
            score = successor.evaluate_objective_function()
            if score < best_score:
                best_cube = copy.deepcopy(successor)  
                best_score = score

        return best_cube
    
    def get_random_successor(self):
        
        return self.generate_random_successor()



# Contoh penggunaan:
# n = 5 
# magic_cube = Cube(n)
# magic_cube.generate_cube()
# magic_cube.display_cube()

# Hitung fungsi objektif
# objective_value = magic_cube.evaluate_objective_function()
# print(f"Objective value (total difference from magic number): {objective_value}")

# Menghasilkan semua successors dan memilih salah satu
# best_cube, best_score = magic_cube.get_best_successor()

# Tampilkan hasil
# print(f"Best score successor has objective value: {best_score}")
# best_cube.display_cube()
