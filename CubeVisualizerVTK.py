import vtk

class CubeVisualizerVTK:
    def __init__(self, cube):
        self.cube = cube  
        
        self.renderer = vtk.vtkRenderer()
        self.render_window = vtk.vtkRenderWindow()
        self.render_window.SetSize(700, 700)
        self.render_window.AddRenderer(self.renderer)
        
        self.render_window_interactor = vtk.vtkRenderWindowInteractor()
        self.render_window_interactor.SetRenderWindow(self.render_window)

        self.cube_size = 3000.0
        self.grid_spacing = self.cube_size
        self.layer_spacing = self.cube_size * 3.5

        self.display_layers_with_cubes()

        self.render_window_interactor.AddObserver("ExitEvent", self.on_exit)

        self.render_window.Render()
        self.setup_interactor()
        self.render_window_interactor.Start()

    def create_text_actor(self, text, position, orientation=(0, 0, 0), scale=(50.0, 50.0, 50.0)):
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
        cube_source = vtk.vtkCubeSource()
        cube_source.SetXLength(self.cube_size)
        cube_source.SetYLength(self.cube_size)
        cube_source.SetZLength(self.cube_size)
        cube_source.SetCenter(position)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cube_source.GetOutputPort())

        cube_actor = vtk.vtkActor()
        cube_actor.SetMapper(mapper)
        cube_actor.GetProperty().SetColor(0.8, 0.8, 1.0)  
        cube_actor.GetProperty().SetOpacity(1.0)
        cube_actor.GetProperty().LightingOff()
        cube_actor.GetProperty().EdgeVisibilityOn()
        cube_actor.GetProperty().SetEdgeColor(0, 0, 0) 
        return cube_actor

    def display_layers_with_cubes(self):
        n = self.cube.size
        self.renderer.RemoveAllViewProps()

        for i in range(n):
            layer = self.cube.cube[i, :, :]

            for j in range(n):
                for k in range(n):
                    value = str(layer[j, k])
                    cube_position = (k * self.grid_spacing, -i * self.layer_spacing, j * self.grid_spacing)

                    self.renderer.AddActor(self.create_cube_actor(cube_position))

                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing, -i * self.layer_spacing + self.cube_size / 2 + 20, j * self.grid_spacing), (-90, 0, 0)))
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing, -i * self.layer_spacing - self.cube_size / 2 - 20, j * self.grid_spacing), (90, 0, 0)))
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing, -i * self.layer_spacing, j * self.grid_spacing - self.cube_size / 2 - 20), (0, 180, 0)))
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing, -i * self.layer_spacing, j * self.grid_spacing + self.cube_size / 2 + 20), (0, 0, 0)))
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing - self.cube_size / 2 - 20, -i * self.layer_spacing, j * self.grid_spacing), (0, -90, 0)))
                    self.renderer.AddActor(self.create_text_actor(value, (k * self.grid_spacing + self.cube_size / 2 + 20, -i * self.layer_spacing, j * self.grid_spacing), (0, 90, 0)))

        self.render_window.Render()

    def setup_interactor(self):
        camera = self.renderer.GetActiveCamera()

        def zoom_in():
            camera.Zoom(1.1)
            self.render_window.Render()

        def zoom_out():
            camera.Zoom(0.9)
            self.render_window.Render()

        style = vtk.vtkInteractorStyleTrackballCamera()
        self.render_window_interactor.SetInteractorStyle(style)

        self.render_window_interactor.AddObserver("KeyPressEvent", lambda : self.on_key_press(zoom_in, zoom_out))

    def on_key_press(self, zoom_in, zoom_out):
        key = self.render_window_interactor.GetKeySym()
        if key == "Up":
            zoom_in()
        elif key == "Down":
            zoom_out()

    def on_exit(self, *args):
        self.render_window.Finalize()
        self.render_window_interactor.TerminateApp()
