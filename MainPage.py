import tkinter as tk
from tkinter import ttk


class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Select an Algorithm", font=("Helvetica", 16))
        label.pack(pady=20)

        sahc_button = ttk.Button(self, text="Steepest Ascent Algorithm",
                               command=lambda: controller.show_frame("SteepestAscentHCPage"))
        sahc_button.pack(pady=10)
        
        rrhc_button = ttk.Button(self, text="Random Restart Hill Climbing Algorithm",
                                command=lambda: controller.show_frame("RandomRestartHCPage"))
        rrhc_button.pack(pady=10)
        
        stochastic_button = ttk.Button(self, text="Stochastic Hill Climbing Algorithm",
                                command=lambda: controller.show_frame("StochasticHCPage"))
        stochastic_button.pack(pady=10)
        
        sideways_move_button = ttk.Button(self, text="Hill Climbing With Sideways Move Algorithm",
                                command=lambda: controller.show_frame("SidewaysMoveHCPage"))
        sideways_move_button.pack(pady=10)

        sa_button = ttk.Button(self, text="Simulated Annealing (SA)", command=lambda: controller.show_frame("SimulatedAnnealingPage"))
        sa_button.pack(pady=10)

        ga_button = ttk.Button(self, text="Genetic Algorithm (GA)", command=self.placeholder)
        ga_button.pack(pady=10)

    def placeholder(self):
        print("Page not implemented yet")