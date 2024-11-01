import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class CubeVisualizer:
    def __init__(self, root, cube):
        self.root = root
        self.cube = cube

        self.figure = Figure(figsize=(6, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.display_cube()

        self.random_button = tk.Button(self.root, text="Generate Random Successor", command=self.generate_random_successor)
        self.random_button.pack()

    def display_cube(self):
        ax = self.figure.add_subplot(111, projection='3d')
        ax.clear()  
        n = self.cube.size
        offset = 1.5  
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    ax.bar3d(i + offset * i, j + offset * j, k + offset * k, 1, 1, 1, shade=True, color='lightblue', edgecolor='black', alpha=0.3)

                    ax.text(i + 0.5 + offset * i, j + 0.5 + offset * j, k + 0.5 + offset * k,
                            str(self.cube.cube[i, j, k]), color='black', ha='center', va='center', fontsize=12, weight='bold')

        ax.view_init(elev=30, azim=45)

        ax.set_box_aspect([1, 1, 1]) 
        self.canvas.draw()

    def generate_random_successor(self):
        self.cube = self.cube.generate_random_successor()
        self.display_cube()  
