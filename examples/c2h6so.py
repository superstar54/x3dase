from ase.build import molecule
from x3dase.x3d import X3D

atoms = molecule('C2H6SO')
X3D(atoms).write('c2h6so.html')