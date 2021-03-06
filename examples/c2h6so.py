from ase.build import molecule
from x3dase.x3d import X3D

atoms = molecule('C2H6SO')
X3D(atoms, bond = 1.0, label = True).write('c2h6so.html')
atoms = molecule('H2O')
X3D(atoms, bond = 1.0, label = True).write('h2o.html')