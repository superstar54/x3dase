from ase.io.cube import read_cube_data
from x3dase.x3d import X3D

data, atoms = read_cube_data('datas/test.cube')
atoms.pbc = [True, True, True]
X3D(atoms, bond = 1.0, label = True, isosurface = [data, -0.001, 0.001]).write('cube.html')