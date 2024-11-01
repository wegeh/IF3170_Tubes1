from Cube import Cube
from CubeVisualizerApp import CubeVisualizerApp
from SteepestAscentHC import SteepestAscentHC

if __name__ == "__main__":
    cube = Cube(5)
    
    
    algorithm = SteepestAscentHC(cube)
    
    res = algorithm.run()
    
    print(res)
    
    

    # app = CubeVisualizerApp(cube, algorithm)
