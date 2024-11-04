import numpy as np
import random
import itertools
import copy
from concurrent.futures import ThreadPoolExecutor

class Cube:
    def __init__(self, n):
        self.size = n
        self.magic_number = n * (n**3 + 1) // 2
        self.cube = np.zeros((n, n, n), dtype=int)
        
        self.row_sums = np.zeros((n, n), dtype=int)  
        self.col_sums = np.zeros((n, n), dtype=int)  
        self.pillar_sums = np.zeros((n, n), dtype=int)  
        self.main_diag_sums = np.zeros(4, dtype=int) 
        self.plane_diag_sums = np.zeros(12, dtype=int) 
    

    def generate_cube(self):
        numbers = np.arange(1, self.size ** 3 + 1)
        np.random.shuffle(numbers)
        self.cube = numbers.reshape((self.size, self.size, self.size))
        self.initialize_sums()


    def swap(self, idx1, idx2):
        i1, j1, k1 = idx1
        i2, j2, k2 = idx2
    
        self.cube[i1, j1, k1], self.cube[i2, j2, k2] = self.cube[i2, j2, k2], self.cube[i1, j1, k1]
        
    
    
    def evaluate_objective_function(self):
        n = self.size
        magic_number = self.magic_number

        row_sums = np.sum(self.cube, axis=2)  
        col_sums = np.sum(self.cube, axis=1)  
        pillar_sums = np.sum(self.cube, axis=0)  
       

        total_diff = np.sum(np.abs(row_sums - magic_number))
        total_diff += np.sum(np.abs(col_sums - magic_number))
        total_diff += np.sum(np.abs(pillar_sums - magic_number))
    
        main_diag_1 = np.sum([self.cube[i, i, i] for i in range(n)])  
        main_diag_2 = np.sum([self.cube[i, i, n-1-i] for i in range(n)])  
        main_diag_3 = np.sum([self.cube[i, n-1-i, i] for i in range(n)])  
        main_diag_4 = np.sum([self.cube[i, n-1-i, n-1-i] for i in range(n)]) 
        

        total_diff += np.abs(main_diag_1 - magic_number)
        total_diff += np.abs(main_diag_2 - magic_number)
        total_diff += np.abs(main_diag_3 - magic_number)
        total_diff += np.abs(main_diag_4 - magic_number)
        

        plane_diag_1 = np.sum([self.cube[i, i, 0] for i in range(n)])  
        plane_diag_2 = np.sum([self.cube[i, n-1-i, 0] for i in range(n)])  
        plane_diag_3 = np.sum([self.cube[i, i, n-1] for i in range(n)]) #tt
        plane_diag_4 = np.sum([self.cube[i, n-1-i, n-1] for i in range(n)])  
        
        plane_diag_5 = np.sum([self.cube[i, 0, i] for i in range(n)])  
        plane_diag_6 = np.sum([self.cube[i, 0, n-1-i] for i in range(n)])  
        plane_diag_7 = np.sum([self.cube[i, n-1, i] for i in range(n)])  
        plane_diag_8 = np.sum([self.cube[i, n-1, n-1-i] for i in range(n)])  
        
        plane_diag_9 = np.sum([self.cube[0, i, i] for i in range(n)])  
        plane_diag_10 = np.sum([self.cube[0, i, n-1-i] for i in range(n)])  #tt
        plane_diag_11 = np.sum([self.cube[n-1, i, i] for i in range(n)])  
        plane_diag_12 = np.sum([self.cube[n-1, i, n-1-i] for i in range(n)])  
    
        
        total_diff += np.abs(plane_diag_1 - magic_number)
        total_diff += np.abs(plane_diag_2 - magic_number)
        total_diff += np.abs(plane_diag_3 - magic_number)
        total_diff += np.abs(plane_diag_4 - magic_number)
        total_diff += np.abs(plane_diag_5 - magic_number)
        total_diff += np.abs(plane_diag_6 - magic_number)
        total_diff += np.abs(plane_diag_7 - magic_number)
        total_diff += np.abs(plane_diag_8 - magic_number)
        total_diff += np.abs(plane_diag_9 - magic_number)
        total_diff += np.abs(plane_diag_10 - magic_number)
        total_diff += np.abs(plane_diag_11 - magic_number)
        total_diff += np.abs(plane_diag_12 - magic_number)
        

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

    def get_best_successor(self) -> 'Cube':
        
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
    
    def to_flat_list(self):
        return self.cube.flatten().tolist()
    
    def from_flat_list(flat_list):
        size = int(round(len(flat_list) ** (1/3)))
        cube = Cube(size)
        cube.cube = np.array(flat_list).reshape((size, size, size))
        return cube
    
    def update_sums_after_swap(self, idx1, idx2):
        i1, j1, k1 = idx1
        i2, j2, k2 = idx2
        n = self.size

        self.row_sums[i1, j1] = np.sum(self.cube[i1, j1, :])
        self.row_sums[i2, j2] = np.sum(self.cube[i2, j2, :])
        self.col_sums[i1, k1] = np.sum(self.cube[i1, :, k1])
        self.col_sums[i2, k2] = np.sum(self.cube[i2, :, k2])
        self.pillar_sums[j1, k1] = np.sum(self.cube[:, j1, k1])
        self.pillar_sums[j2, k2] = np.sum(self.cube[:, j2, k2])

        if (i1 == j1 == k1) or (i2 == j2 == k2):
            self.main_diag_sums[0] = np.sum([self.cube[i, i, i] for i in range(n)])  
            # print("a1")
        if (i1 == j1 == n-1-k1) or (i2 == j2 == n-1-k2):
            self.main_diag_sums[1] = np.sum([self.cube[i, i, n-1-i] for i in range(n)])  
            # print("a2")
        if (i1 == n-1-j1 == k1) or (i2 == n-1-j2 == k2):
            self.main_diag_sums[2] = np.sum([self.cube[i, n-1-i, i] for i in range(n)])
            # print("a3") 
        if (i1 == n-1-j1 == n-1-k1) or (i2 == n-1-j2 == n-1-k2):
            self.main_diag_sums[3] = np.sum([self.cube[i, n-1-i, n-1-i] for i in range(n)])
            # print("a4")  

        if (i1 == j1 == 0) or (i2 == j2 == 0):
            self.plane_diag_sums[0] = np.sum([self.cube[i, i, 0] for i in range(n)])  
            # print("b1")  
        if (i1 == n-1-j1 == 0) or (i2 == n-1-j2 == 0):
            self.plane_diag_sums[1] = np.sum([self.cube[i, n-1-i, 0] for i in range(n)])  
            # print("b2")
        if (i1 == j1 == n-1) or (i2 == j2 == n-1):
            self.plane_diag_sums[2] = np.sum([self.cube[i, i, n-1] for i in range(n)])
            # print("b3") 
        if (i1 == n-1-j1 == n-1) or (i2 == n-1-j2 == n-1):
            self.plane_diag_sums[3] = np.sum([self.cube[i, n-1-i, n-1] for i in range(n)])  
            # print("b4")
            

        if (i1 == 0 == k1) or (i2 == 0 == k2):
            self.plane_diag_sums[4] = np.sum([self.cube[i, 0, i] for i in range(n)]) 
            # print("c1") 
        if (i1 == 0 == n-1-k1) or (i2 == 0 == n-1-k2):
            self.plane_diag_sums[5] = np.sum([self.cube[i, 0, n-1-i] for i in range(n)]) 
            # print("c2") 
        if (i1 == n-1 == k1) or (i2 == n-1 == k2):
            self.plane_diag_sums[6] = np.sum([self.cube[i, n-1, i] for i in range(n)])  
            # print("c3")
        if (i1 == n-1 == n-1-k1) or (i2 == n-1 == n-1-k2):
            self.plane_diag_sums[7] = np.sum([self.cube[i, n-1, n-1-i] for i in range(n)]) 
            # print("c4") 

        if (j1 == 0 == k1) or (j2 == 0 == k2):
            self.plane_diag_sums[8] = np.sum([self.cube[0, i, i] for i in range(n)])
            # print("d1")  
        if (j1 == 0 == n-1-k1) or (j2 == 0 == n-1-k2):
            self.plane_diag_sums[9] = np.sum([self.cube[0, i, n-1-i] for i in range(n)]) 
            # print("d2")
        if (j1 == n-1 == k1) or (j2 == n-1 == k2):
            self.plane_diag_sums[10] = np.sum([self.cube[n-1, i, i] for i in range(n)]) 
            # print("d3") 
        if (j1 == n-1 == n-1-k1) or (j2 == n-1 == n-1-k2):
            self.plane_diag_sums[11] = np.sum([self.cube[n-1, i, n-1-i] for i in range(n)])  
            # print("d4")

    def swap_and_update(self, idx1, idx2):
        self.swap(idx1, idx2)  
        # self.display_cube()
        self.update_sums_after_swap(idx1, idx2) 
        
    def evaluate_objective_function4(self):
        n = self.size
        magic_number = self.magic_number

        def compute_sums():
            row_sums = np.sum(self.cube, axis=2)
            col_sums = np.sum(self.cube, axis=1)
            pillar_sums = np.sum(self.cube, axis=0)
            return row_sums, col_sums, pillar_sums

        def compute_main_diagonals():
            main_diag_1 = np.sum([self.cube[i, i, i] for i in range(n)])
            main_diag_2 = np.sum([self.cube[i, i, n-1-i] for i in range(n)])
            main_diag_3 = np.sum([self.cube[i, n-1-i, i] for i in range(n)])
            main_diag_4 = np.sum([self.cube[i, n-1-i, n-1-i] for i in range(n)])
            return [main_diag_1, main_diag_2, main_diag_3, main_diag_4]

        def compute_plane_diagonals():
            plane_diagonals = [
                np.sum([self.cube[i, i, 0] for i in range(n)]),
                np.sum([self.cube[i, n-1-i, 0] for i in range(n)]),
                np.sum([self.cube[i, i, n-1] for i in range(n)]),
                np.sum([self.cube[i, n-1-i, n-1] for i in range(n)]),
                np.sum([self.cube[i, 0, i] for i in range(n)]),
                np.sum([self.cube[i, 0, n-1-i] for i in range(n)]),
                np.sum([self.cube[i, n-1, i] for i in range(n)]),
                np.sum([self.cube[i, n-1, n-1-i] for i in range(n)]),
                np.sum([self.cube[0, i, i] for i in range(n)]),
                np.sum([self.cube[0, i, n-1-i] for i in range(n)]),
                np.sum([self.cube[n-1, i, i] for i in range(n)]),
                np.sum([self.cube[n-1, i, n-1-i] for i in range(n)]),
            ]
            return plane_diagonals

        total_diff = 0

        with ThreadPoolExecutor() as executor:
            future_sums = executor.submit(compute_sums)
            row_sums, col_sums, pillar_sums = future_sums.result()

            total_diff += np.sum(np.abs(row_sums - magic_number))
            total_diff += np.sum(np.abs(col_sums - magic_number))
            total_diff += np.sum(np.abs(pillar_sums - magic_number))

            future_main_diags = executor.submit(compute_main_diagonals)
            future_plane_diags = executor.submit(compute_plane_diagonals)

            main_diags = future_main_diags.result()
            plane_diags = future_plane_diags.result()

            total_diff += sum(np.abs(diag - magic_number) for diag in main_diags)
            total_diff += sum(np.abs(diag - magic_number) for diag in plane_diags)

        return total_diff
    
    def evaluate_objective_function3(self):
        n = self.size
        magic_number = self.magic_number

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_results = [
                executor.submit(np.sum, self.cube, axis=2),  
                executor.submit(np.sum, self.cube, axis=1),  
                executor.submit(np.sum, self.cube, axis=0), 
                executor.submit(lambda: np.sum([self.cube[i, i, i] for i in range(n)])), 
                executor.submit(lambda: np.sum([self.cube[i, i, n-1-i] for i in range(n)])), 
                executor.submit(lambda: np.sum([self.cube[i, n-1-i, i] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[i, n-1-i, n-1-i] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[i, i, 0] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[i, n-1-i, 0] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[i, i, n-1] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[i, n-1-i, n-1] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[i, 0, i] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[i, 0, n-1-i] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[i, n-1, i] for i in range(n)])),
                executor.submit(lambda: np.sum([self.cube[i, n-1, n-1-i] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[0, i, i] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[0, i, n-1-i] for i in range(n)])), 
                executor.submit(lambda: np.sum([self.cube[n-1, i, i] for i in range(n)])),  
                executor.submit(lambda: np.sum([self.cube[n-1, i, n-1-i] for i in range(n)])), 
            ]

            results = [future.result() for future in future_results]

            total_diff = 0
            total_diff += np.sum(np.abs(results[0] - magic_number))
            total_diff += np.sum(np.abs(results[1] - magic_number))
            total_diff += np.sum(np.abs(results[2] - magic_number))
            total_diff += sum(np.abs(results[i] - magic_number) for i in range(3, 7))
            total_diff += sum(np.abs(results[i] - magic_number) for i in range(7, len(results)))

        return total_diff   
    
    def evaluate_objective_function2(self):
        magic_number = self.magic_number
        total_diff = 0
        
        total_diff += np.sum(np.abs(self.row_sums - magic_number))
        total_diff += np.sum(np.abs(self.col_sums - magic_number))
        total_diff += np.sum(np.abs(self.pillar_sums - magic_number))
        total_diff += np.sum(np.abs(self.main_diag_sums - magic_number))
        total_diff += np.sum(np.abs(self.plane_diag_sums - magic_number))
        
        return total_diff
    
    def __str__(self):
        return f"Cube of size {self.size}x{self.size}\n" + "\n".join([str(row) for row in self.cube])
    
    
    def display_cube(self):
        for layer in self.cube:
            print(layer)
            print() 
            
    def initialize_sums(self):
        n = self.size
        self.row_sums = np.sum(self.cube, axis=2)
        self.col_sums = np.sum(self.cube, axis=1)
        self.pillar_sums = np.sum(self.cube, axis=0)

        self.main_diag_sums[0] = np.sum([self.cube[i, i, i] for i in range(n)])
        self.main_diag_sums[1] = np.sum([self.cube[i, i, n-1-i] for i in range(n)])
        self.main_diag_sums[2] = np.sum([self.cube[i, n-1-i, i] for i in range(n)])
        self.main_diag_sums[3] = np.sum([self.cube[i, n-1-i, n-1-i] for i in range(n)])

        self.plane_diag_sums[0] = np.sum([self.cube[i, i, 0] for i in range(n)])
        self.plane_diag_sums[1] = np.sum([self.cube[i, n-1-i, 0] for i in range(n)])
        self.plane_diag_sums[2] = np.sum([self.cube[i, i, n-1] for i in range(n)]) #tt
        self.plane_diag_sums[3] = np.sum([self.cube[i, n-1-i, n-1] for i in range(n)])
        self.plane_diag_sums[4] = np.sum([self.cube[i, 0, i] for i in range(n)])
        self.plane_diag_sums[5] = np.sum([self.cube[i, 0, n-1-i] for i in range(n)])
        self.plane_diag_sums[6] = np.sum([self.cube[i, n-1, i] for i in range(n)])
        self.plane_diag_sums[7] = np.sum([self.cube[i, n-1, n-1-i] for i in range(n)])
        self.plane_diag_sums[8] = np.sum([self.cube[0, i, i] for i in range(n)])
        self.plane_diag_sums[9] = np.sum([self.cube[0, i, n-1-i] for i in range(n)]) #tt
        self.plane_diag_sums[10] = np.sum([self.cube[n-1, i, i] for i in range(n)])
        self.plane_diag_sums[11] = np.sum([self.cube[n-1, i, n-1-i] for i in range(n)])

    