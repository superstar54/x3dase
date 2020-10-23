from ase.io import read, write
from x3dase.x3d import write_html

atoms = read('datas/perovskite.cif')
atoms.pbc = [True, True, True]
atoms = atoms*[2, 2, 2]
kind_props = {
'Pb': {'radius': 1.0, 'color': [100/255.0, 191/255.0, 56/255.0]},
'O': {'radius': 1.0, }
}
write_html('perovskite.html', atoms, show_unit_cell = True, bond = 1.0, scale = 0.6, polyhedra_dict =  {'Pb': ['I']})