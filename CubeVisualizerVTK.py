import tkinter as tk
from tkinter import ttk
import vtk


class CubeVisualizerApp:
    def __init__(self, cube):
        self.cube = cube  # Instance dari class Cube yang berisi data cube
        
        # Setup tkinter window for 2D
        self.root = tk.Tk()
        self.root.title("Cube Visualizer")
        self.root.geometry("900x600")

        # Create 2D container
        self.frame_2d = tk.Frame(self.root)
        self.frame_2d.pack(expand=True, fill="both")

        # Create the 3D button
        self.frame_3d_button = tk.Frame(self.root)
        self.frame_3d_button.pack(fill="x")
        start_3d_button = tk.Button(self.frame_3d_button, text="Switch to 3D", command=self.open_3d_window)
        start_3d_button.pack(pady=20)

        # Initialize the 2D view
        self.create_2d_view()

        # Start the Tkinter main loop
        self.root.mainloop()

    def create_2d_view(self):
        """ Menampilkan representasi 2D dari cube menggunakan tkinter grid yang lebih rapi. """
        n = self.cube.size

        # Buat canvas dengan scrollbar untuk 2D view
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

        # Menampilkan angka dalam bentuk grid
        max_columns = 3  # Limit the number of columns to prevent it from extending too far vertically
        for i in range(n):
            layer_frame = tk.Frame(scrollable_frame)
            layer_frame.grid(row=i // max_columns, column=i % max_columns, padx=20, pady=20)

            tk.Label(layer_frame, text=f"Layer {i+1}", font=("Arial", 14)).pack()

            for j in range(n):
                row_frame = tk.Frame(layer_frame)
                row_frame.pack()
                for k in range(n):
                    value = str(self.cube.cube[i, j, k])
                    tk.Label(row_frame, text=value, borderwidth=1, relief="solid", width=5, height=2).pack(side=tk.LEFT, padx=5, pady=5)

    def open_3d_window(self):
        """ Membuka tampilan 3D dalam window terpisah tanpa mempengaruhi tampilan 2D. """
        CubeVisualizerVTK(self.cube)  # Create 3D window without destroying 2D


class CubeVisualizerVTK:
    def __init__(self, cube):
        self.cube = cube  # Instance dari class Cube yang berisi data cube

        # Setup VTK renderer and window
        self.renderer = vtk.vtkRenderer()
        self.render_window = vtk.vtkRenderWindow()
        self.render_window.SetSize(700, 700)
        self.render_window.AddRenderer(self.renderer)
        
        # Interactor to allow interaction
        self.render_window_interactor = vtk.vtkRenderWindowInteractor()
        self.render_window_interactor.SetRenderWindow(self.render_window)

        # Cube configuration
        self.cube_size = 3000.0
        self.grid_spacing = self.cube_size
        self.layer_spacing = self.cube_size * 3.5

        # Display cube and numbers on all sides
        self.display_layers_with_cubes()

        # Hook window close event to clean up resources
        self.render_window_interactor.AddObserver("ExitEvent", self.on_exit)

        # Render and start interactor
        self.render_window.Render()
        self.setup_interactor()
        self.render_window_interactor.Start()

    def create_text_actor(self, text, position, orientation=(0, 0, 0), scale=(50.0, 50.0, 50.0)):
        """ Membuat aktor teks 3D untuk menampilkan angka di posisi tertentu. """
        text_actor = vtk.vtkTextActor3D()
        text_actor.SetInput(text)
        text_actor.SetPosition(position)
        text_actor.SetScale(scale)
        text_actor.GetTextProperty().SetFontSize(26)
        text_actor.GetTextProperty().SetColor(0, 0, 0)
        text_actor.GetTextProperty().BoldOn()
        text_actor.GetTextProperty().SetJustificationToCentered()
        text_actor.SetOrientation(orientation)
        return text_actor

    def create_cube_actor(self, position):
        """ Membuat aktor cube 3D untuk setiap angka. """
        cube_source = vtk.vtkCubeSource()
        cube_source.SetXLength(self.cube_size)
        cube_source.SetYLength(self.cube_size)
        cube_source.SetZLength(self.cube_size)
        cube_source.SetCenter(position)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cube_source.GetOutputPort())

        cube_actor = vtk.vtkActor()
        cube_actor.SetMapper(mapper)
        cube_actor.GetProperty().SetColor(0.8, 0.8, 1.0)  # Warna biru muda
        cube_actor.GetProperty().SetOpacity(1.0)
        cube_actor.GetProperty().LightingOff()
        cube_actor.GetProperty().EdgeVisibilityOn()
        cube_actor.GetProperty().SetEdgeColor(0, 0, 0)  # Border hitam
        return cube_actor

    def display_layers_with_cubes(self):
        """ Menampilkan layer cube sebagai tumpukan dengan angka di tiap sisi. """
        n = self.cube.size
        self.renderer.RemoveAllViewProps()

        for i in range(n):
            layer = self.cube.cube[i, :, :]

            for j in range(n):
                for k in range(n):
                    value = str(layer[j, k])
                    cube_position = (k * self.grid_spacing, -i * self.layer_spacing, -j * self.grid_spacing)

                    # Add cube
                    self.renderer.AddActor(self.create_cube_actor(cube_position))

                    # Add text on each side
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing, -i * self.layer_spacing + self.cube_size / 2 + 20, -j * self.grid_spacing), (-90, 0, 0)))
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing, -i * self.layer_spacing - self.cube_size / 2 - 20, -j * self.grid_spacing), (90, 0, 0)))
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing, -i * self.layer_spacing, -j * self.grid_spacing - self.cube_size / 2 - 20), (0, 180, 0)))
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing, -i * self.layer_spacing, -j * self.grid_spacing + self.cube_size / 2 + 20), (0, 0, 0)))
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing - self.cube_size / 2 - 20, -i * self.layer_spacing, -j * self.grid_spacing), (0, -90, 0)))
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing + self.cube_size / 2 + 20, -i * self.layer_spacing, -j * self.grid_spacing), (0, 90, 0)))

        self.render_window.Render()

    def setup_interactor(self):
        """ Mengatur interaksi kamera untuk zoom in/out. """
        camera = self.renderer.GetActiveCamera()

        def zoom_in():
            camera.Zoom(1.1)
            self.render_window.Render()

        def zoom_out():
            camera.Zoom(0.9)
            self.render_window.Render()

        style = vtk.vtkInteractorStyleTrackballCamera()
        self.render_window_interactor.SetInteractorStyle(style)

        self.render_window_interactor.AddObserver("KeyPressEvent", lambda obj, event: self.on_key_press(obj, event, zoom_in, zoom_out))

    def on_key_press(self, obj, event, zoom_in, zoom_out):
        """ Event handler untuk keyboard zoom. """
        key = self.render_window_interactor.GetKeySym()
        if key == "Up":
            zoom_in()
        elif key == "Down":
            zoom_out()

    def on_exit(self, obj, event):
        """ Callback saat 3D view ditutup. """
        self.render_window.Finalize()
        self.render_window_interactor.TerminateApp()
