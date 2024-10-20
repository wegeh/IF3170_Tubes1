from Cube import Cube
from CubeVisualizerVTK import CubeVisualizerApp

if __name__ == "__main__":
    # Initialize the Cube object (assuming size 4 here)
    cube = Cube(5)
    cube.generate_cube()  # Generate the random cube

    # Start the visualizer app
    app = CubeVisualizerApp(cube)
