import tkinter as tk
from MainPage import MainPage
from SteepestAscentHCPage import SteepestAscentHCPage
from RandomRestartHCPage import RandomRestartHCPage
from StochasticHCPage import StochasticHCPage
from SidewaysMoveHCPage import SidewaysMoveHCPage
from SimulatedAnnealingPage import SimulatedAnnealingPage
from GeneticAlgorithmPage import GeneticAlgorithmPage
import signal
import os


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TUBES ARTIFICIAL INTELLIGENCE")
        self.geometry("800x600")
        self.frames = {}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_frames()
        self.child_processes = []
        
        self.show_frame("MainPage")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_frames(self):
        for F in (MainPage, SteepestAscentHCPage, RandomRestartHCPage, StochasticHCPage, SidewaysMoveHCPage, SimulatedAnnealingPage, GeneticAlgorithmPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
    def on_close(self):
        for process in self.child_processes:
            if process.is_alive():
                os.kill(process.pid, signal.SIGTERM)  
        self.destroy()
        os._exit(1)