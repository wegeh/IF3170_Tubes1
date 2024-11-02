import tkinter as tk
from tkinter import ttk


class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Select an Algorithm", font=("Helvetica", 16))
        label.pack(pady=20)

        sa_button = ttk.Button(self, text="Steepest Ascent Algorithm",
                               command=lambda: controller.show_frame("SteepestAscentPage"))
        sa_button.pack(pady=10)

        sa_button = ttk.Button(self, text="Simulated Annealing (SA)", command=self.placeholder)
        sa_button.pack(pady=10)

        ga_button = ttk.Button(self, text="Genetic Algorithm (GA)", command=self.placeholder)
        ga_button.pack(pady=10)

    def placeholder(self):
        print("Page not implemented yet")