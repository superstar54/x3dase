from ase.io.cube import read_cube_data
from x3dase.x3d import write_html

data, atoms = read_cube_data('datas/test.cube')
atoms.pbc = [True, True, True]
print(atoms)
write_html('cube.html', atoms, isosurface = [data, -0.001, 0.001])