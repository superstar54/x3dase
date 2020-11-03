#!/usr/bin/env python3
from x3dase.visualize import view_x3d
from x3dase import X3D
from ase.build import fcc111
atoms = fcc111('Pt', size=(1, 1, 3), vacuum = 5.0)
atoms = atoms*[1, 1, 1]
print(len(atoms))
atoms.positions[:, 2] -= min(atoms.positions[:, 2])
# X3D(atoms, bond=1.0).write('pt-111.html')
X3D(atoms, label = True, bond = 1.0).write('pt-111.html')
