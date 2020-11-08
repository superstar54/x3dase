from ase.io import read, write
from x3dase.x3d import X3D

atoms = read('datas/perovskite.cif')
atoms.pbc = [True, True, True]
atoms = atoms*[2, 2, 2]
X3D(atoms, bond = 1.0, rmbonds = {'Pb': ['Pb']}, label = True, polyhedra =  {'Pb': ['I']}).write('perovskite.html')