from ase.io import read, write
from x3dase.x3d import write_html

atoms = read('datas/perovskite.cif')
atoms.pbc = [True, True, True]
atoms = atoms*[2, 2, 2]
write_html('perovskite.html', atoms, show_unit_cell = True, bond = 1.0, polyhedra_dict =  {'Pb': ['I']})