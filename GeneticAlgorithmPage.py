import tkinter as tk
from tkinter import ttk
from Cube import Cube
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
from queue import Queue
import matplotlib.pyplot as plt
from CubeVisualizerVTK import CubeVisualizerVTK
from multiprocessing import Process

class GeneticAlgorithmPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(self)
        canvas.grid(row=0, column=0, sticky="nsew")
        canvas.grid_rowconfigure(0, weight=1)
        canvas.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        

        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.grid_rowconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="frame")

        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int(e.delta/120), "units"))


        label = ttk.Label(scrollable_frame, text="Genetic Algorithm", font=("Helvetica", 16))
        label.pack(pady=20)
        
        self.initial_temp_label = tk.Label(scrollable_frame, text="Initial Temp:")
        self.initial_temp_label.pack(pady=5)
        self.initial_temp_entry = tk.Entry(scrollable_frame)
        self.initial_temp_entry.pack(pady=5)

        start_button = ttk.Button(scrollable_frame, text="Start", command=self.start_genetic_algorithm)
        start_button.pack(pady=10)

        back_button = ttk.Button(scrollable_frame, text="Back to Main Menu",
                                 command=lambda: controller.show_frame("MainPage"))
        back_button.pack(pady=10)

        self.initial_state_frame = ttk.LabelFrame(scrollable_frame, text="Initial State")
        self.initial_state_frame.pack(pady=10, fill="both", expand=True)
        
        self.initial_3d_button = tk.Button(self.initial_state_frame, text="Show 3D Initial State", command=self.show_initial_3d, state="disabled")
        self.initial_3d_button.pack(pady=5)

        self.final_state_frame = ttk.LabelFrame(scrollable_frame, text="Final State")
        self.final_state_frame.pack(pady=10, fill="both", expand=True)
        
        self.final_3d_button = tk.Button(self.final_state_frame, text="Show 3D Final State", command=self.show_final_3d, state="disabled")
        self.final_3d_button.pack(pady=5)
        
        self.plot_frame = tk.Frame(scrollable_frame)
        self.plot_frame.pack(pady=10, fill="both", expand=True)

        self.result_text = tk.Text(scrollable_frame, wrap="word", height=10)
        self.result_text.pack(pady=10, fill="both", expand=True)
        
        

    def start_genetic_algorithm(self):
        self.result_text.delete(1.0, tk.END)
        try:
            initial_temp = int(self.initial_temp_entry.get())
        except ValueError:
            self.result_text.insert(tk.END, "Invalid input for Max Restarts. Please enter an integer.\n")
            return
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Genetic Annealing...\n")
        self.algorithm_running = True
        self.initial_3d_button.config(state="disabled")
        self.final_3d_button.config(state="disabled")
        self.result_queue = Queue()
        thread = Thread(target=self.run_algorithm, args=(initial_temp, self.result_queue))
        thread.start()
        self.after(100, self.check_queue)

    def run_algorithm(self, initial_temp, result_queue):
        cube = Cube(5)
        # algorithm = SimulatedAnnealing(cube, initial_temp)
        # result = algorithm.run()
        # result_queue.put(result)

    def check_queue(self):
        try:
            result = self.result_queue.get_nowait() 
            self.initial_cube = result['initial_state']
            self.final_cube = result['final_state']

            initial_state = self.initial_cube.cube
            final_state = self.final_cube.cube

            self.display_cube_state(self.initial_state_frame, initial_state)
            self.display_cube_state(self.final_state_frame, final_state)
            
            self.initial_3d_button.config(state="normal")
            self.final_3d_button.config(state="normal")

            result_str = (
                f"Final Objective Value: {result['final_objective']}\n"
                f"Frequency Stuck: {result['stuck_frequency']}\n"
                f"Execution Time: {result['duration']:.2f} seconds\n"
            )
            self.result_text.delete(1.0, tk.END)
            
            self.result_text.insert(tk.END, result_str)
            
            self.plot_objective_progress(result['objective_progress'])
            self.plot_probability_progress(result['probability_progress'])
            

        except Exception:
            self.after(100, self.check_queue)
            
    def plot_objective_progress(self, objective_progress):
        
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(objective_progress, label="Objective Value")
        ax.set_title("Objective Function vs Iterations")
        ax.set_xlabel("Iterations")
        ax.set_ylabel("Objective Function Value")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def plot_probability_progress(self, probability_progress):
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(probability_progress, label="Probability (e)", color='green')
        ax.set_title("Probability (e) vs Iterations")
        ax.set_xlabel("Iterations")
        ax.set_ylabel("Probability (e)")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def show_initial_3d(self):
        if self.initial_cube:
            process = Process(target=CubeVisualizerVTK, args=(self.initial_cube,))
            process.start()
            self.controller.child_processes.append(process)

    def show_final_3d(self):
        if self.final_cube:
            process = Process(target=CubeVisualizerVTK, args=(self.final_cube,))
            process.start()
            self.controller.child_processes.append(process)

    def display_cube_state(self, parent, cube_state):
        for widget in parent.winfo_children():
            if not isinstance(widget, tk.Button):  
                widget.destroy()

        n = cube_state.shape[0]

        for i in range(n):
            layer_frame = ttk.LabelFrame(parent, text=f"Layer {i+1}")
            layer_frame.pack(padx=5, pady=5, fill="both", expand=True)

            for j in range(n):
                row_frame = tk.Frame(layer_frame)
                row_frame.pack()
                for k in range(n):
                    value = str(cube_state[i, j, k])
                    entry = tk.Entry(row_frame, width=5, justify="center")
                    entry.insert(0, value)
                    entry.config(state="disabled")
                    entry.pack(side=tk.LEFT, padx=2, pady=2)