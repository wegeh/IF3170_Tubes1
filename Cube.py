import random

class Cube:
    def __init__(self, n):
        self.size = n
        self.magic_number = n * (n**3 + 1) // 2
        self.cube = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)]

    def generate_cube(self):
        numbers = list(range(1, self.size ** 3 + 1))
        random.shuffle(numbers)
        
        index = 0
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    self.cube[i][j][k] = numbers[index]
                    index += 1

    def display_cube(self):
        #print per layer baru print per baris
        for layer in self.cube:
            for row in layer:
                print(row)
            print() 

    def swap(self, idx1, idx2):
        #i = layer, j = baris, k = kolom
        i1, j1, k1 = idx1
        i2, j2, k2 = idx2
    
        self.cube[i1][j1][k1], self.cube[i2][j2][k2] = self.cube[i2][j2][k2], self.cube[i1][j1][k1]
        print(f"Swapped values at {idx1} and {idx2}.")


# Contoh:
# n = 5 
# magic_cube = Cube(n)
# magic_cube.generate_cube()
# magic_cube.display_cube()
# magic_cube.swap((0, 0, 0), (2, 2, 2))
# magic_cube.display_cube()