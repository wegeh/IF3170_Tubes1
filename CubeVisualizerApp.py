import tkinter as tk
from CubeVisualizerVTK import CubeVisualizerVTK
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Cube import Cube

class CubeVisualizerApp:
    def __init__(self, cube: Cube, algorithm):
        self.cube = cube
        self.algorithm = algorithm
        
        self.root = tk.Tk()
        self.root.title("Cube Visualizer")
        self.root.geometry("1200x800")

        self.frame_2d = tk.Frame(self.root)
        self.frame_2d.pack(side=tk.LEFT, expand=True, fill="both")

        self.frame_right = tk.Frame(self.root)
        self.frame_right.pack(side=tk.RIGHT, expand=True, fill="both", padx=10, pady=10)

        self.frame_3d_button = tk.Frame(self.frame_right)
        self.frame_3d_button.pack(fill="x")
        start_3d_button = tk.Button(self.frame_3d_button, text="Switch to 3D", command=self.open_3d_window)
        start_3d_button.pack(pady=20)

        start_experiment_button = tk.Button(self.frame_3d_button, text="Start Experiment", command=self.run_experiment)
        start_experiment_button.pack(pady=20)

        self.experiment_results_frame = tk.Frame(self.frame_right)
        self.experiment_results_frame.pack(expand=True, fill="both")

        self.create_2d_view(self.cube)
        self.root.mainloop()

    def create_2d_view(self, cube: Cube):
        n = cube.size

        canvas = tk.Canvas(self.frame_2d)
        scrollbar = tk.Scrollbar(self.frame_2d, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        max_columns = 3  
        for i in range(n):
            layer_frame = tk.Frame(scrollable_frame)
            layer_frame.grid(row=i // max_columns, column=i % max_columns, padx=20, pady=20)

            tk.Label(layer_frame, text=f"Layer {i+1}", font=("Arial", 14)).pack()

            for j in range(n):
                row_frame = tk.Frame(layer_frame)
                row_frame.pack()
                for k in range(n):
                    value = str(cube.cube[i, j, k])
                    tk.Label(row_frame, text=value, borderwidth=1, relief="solid", width=5, height=2).pack(side=tk.LEFT, padx=5, pady=5)

    def open_3d_window(self):
        CubeVisualizerVTK(self.cube)  

    def run_experiment(self):
        for widget in self.experiment_results_frame.winfo_children():
            widget.destroy()

        result_text = f"Running {self.algorithm.__class__.__name__} algorithm...\n"
        tk.Label(self.experiment_results_frame, text=result_text, font=("Arial", 12)).pack()

        experiment_result = self.algorithm.run()

        result_text = f"""
        Initial Cube State: {experiment_result['initial_state']}
        Final Cube State: {experiment_result['final_state']}
        Final Objective Value: {experiment_result['final_objective']}
        Iterations: {experiment_result['iterations']}
        Duration: {experiment_result['duration']} seconds
        """
        tk.Label(self.experiment_results_frame, text=result_text, font=("Arial", 12)).pack()

        self.plot_objective(experiment_result['objective_progress'])
        self.create_2d_view()
        

    def plot_objective(self, objective_progress):
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot(objective_progress)
        ax.set_title(f'Objective Progression')
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Objective Function Value')

        canvas = FigureCanvasTkAgg(figure, self.experiment_results_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()