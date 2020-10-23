"""
Output support for X3D and X3DOM file types.
See http://www.web3d.org/x3d/specifications/
X3DOM outputs to html pages that should display 3-d manipulatable atoms in
modern web browsers.
"""

from ase.data import covalent_radii
from ase.data.colors import jmol_colors
import numpy as np
from x3dase.tools import get_atom_kinds, get_bond_kinds, build_tag, get_bondpairs
import time


def write_x3d(filename, atoms, format=None):
    """Writes to html using X3DOM.

    Args:
        filename - str or file-like object, filename or output file object
        atoms - Atoms object to be rendered
        format - str, either 'X3DOM' for web-browser compatibility or 'X3D'
            to be readable by Blender. `None` to detect format based on file
            extension ('.html' -> 'X3DOM', '.x3d' -> 'X3D')"""
    X3D(atoms).write(filename, datatype=format)


def write_html(filename, atoms):
    """Writes to html using X3DOM

    Args:
        filename - str or file-like object, filename or output file object
        atoms - Atoms object to be rendered"""
    write_x3d(filename, atoms, format='X3DOM')


class X3D:
    """Class to write either X3D (readable by open-source rendering
    programs such as Blender) or X3DOM html, readable by modern web
    browsers.
    """

    def __init__(self, atoms, show_unit_cell = None, **kwargs):
        self._atoms = atoms
        self.show_unit_cell = show_unit_cell
        self.atom_kinds = get_atom_kinds(atoms)
        bondlist = get_bondpairs(atoms)
        self.bond_kinds = get_bond_kinds(atoms, self.atom_kinds, bondlist)

    def write(self, filename, datatype=None, **kwargs):
        """Writes output to either an 'X3D' or an 'X3DOM' file, based on
        the extension. For X3D, filename should end in '.x3d'. For X3DOM,
        filename should end in '.html'.

        Args:
            filename - str or file-like object, output file name or writer
            datatype - str, output format. 'X3D' or 'X3DOM'. If `None`, format
                will be determined from the filename"""

        out, tail = write_header_tail(datatype, filename)
        out.append('<Scene>\n')
        atomic_str = self.draw_atoms()
        out.extend(atomic_str)
        cell_str = self.draw_cells()
        out.extend(cell_str)
        bond_str = self.draw_bonds()
        out.extend(bond_str)
        out.append('</Scene>\n')
        out.extend(tail)
        # w = WriteToFile(filename, 'w')
        if isinstance(filename, str):
            with open(filename, 'w') as f:
                f.write(''.join(out))
        else:
            f = filename
            f.write(''.join(out))


    def draw_atoms(self):
        '''
        Draw atoms
        bsdf_inputs: dict
            The key and value for principled_bsdf node
        material_style: string
            Select materials type from ['blase', 'glass', 'ceramic', 'plastic'].
        '''
        # build materials
        atomic_str = ''
        for kind, datas in self.atom_kinds.items():
            tstart = time.time()
            material = build_tag('Material', **datas['material'])
            sphere = build_tag('Sphere', **datas['sphere'])
            appearance = build_tag('Appearance', body=material)
            shape = build_tag('Shape', name=kind, body = appearance + sphere)
            switch = build_tag('Switch', body = shape, whichChoice = "-1")
            atomic_str += switch
            for pos in datas['positions']:
                shape1 = build_tag('Shape', use=kind)
                atomic_str += build_tag('Transform', body=shape1, translation = tuple(pos))
            # print('atoms: {0}   {1:10.2f} s'.format(kind, time.time() - tstart))
        atomic_str = build_tag('Group', onclick="handleGroupClick(event)", body = atomic_str)
        return atomic_str
    def draw_cells(self, celllinewidth = 0.05):
        """
        Draw unit cell
        """
        cell_str = []
        if self._atoms.pbc.any():
            cell = self._atoms.cell
            cell_vertices = np.empty((2, 2, 2, 3))
            for c1 in range(2):
                for c2 in range(2):
                    for c3 in range(2):
                        cell_vertices[c1, c2, c3] = np.dot([c1, c2, c3],
                                                            cell)
            cell_vertices.shape = (1, 24)
            cell_vertices = cell_vertices
            # edges
            coordIndex =      '0 1 -1 0 2 -1 0 4 -1 1 3 -1 1 5 -1 2 3 -1 2 6 -1 3 7 -1 4 5 -1 4 6 -1 5 7 -1 6 7 -1'
            # coordIndex = '0 1 2 3 0 -1 4 5 6 7 4 -1 0 4 -1 1 5 -1 2 6 -1 3 7'
            point = str(cell_vertices)
            cell_str = '''
            <Shape>
            <Appearance>
            <Material diffuseColor='0 0 0' emissiveColor='0 0.5 1'/>
            </Appearance>
            <IndexedLineSet coordIndex='%s'>
            <Coordinate point='%s'/>
            </IndexedLineSet>
            </Shape>
            '''%(coordIndex, point)
        return cell_str

    def draw_bonds(self):
        '''
        Draw atom bonds
        '''
        # build materials
        bond_str = ''
        for kind, datas in self.bond_kinds.items():
            tstart = time.time()
            material = build_tag('Material', **datas['material'])
            sphere = build_tag('Cylinder', height = 1.0, radius = 0.1)
            appearance = build_tag('Appearance', body=material)
            shape = build_tag('Shape', name=kind, body = appearance + sphere)
            switch = build_tag('Switch', body = shape, whichChoice = "-1")
            bond_str += switch
            for pos, height, rotation in zip(datas['centers'], datas['lengths'], datas['rotations']):
                shape1 = build_tag('Shape', use=kind)
                bond_str += build_tag('Transform', body=shape1, translation = tuple(pos), scale = (1, height, 1), rotation = rotation)
            # print('bond: {0}   {1:10.2f} s'.format(kind, time.time() - tstart))
        bond_str = build_tag('Group', onclick="handleGroupClick(event)", body = bond_str)
        return bond_str

class WriteToFile:
    """Creates convenience function to write to a file."""

    def __init__(self, filename, mode='w'):
        if isinstance(filename, str):
            self._f = open(filename, mode)
        else:
            self._f = filename

    def __call__(self, indent, line):
        text = ' ' * indent
        print('%s%s\n' % (text, line), file=self._f)

    def close(self):
        self._f.close()



def write_header_tail(datatype, filename):
    from x3dase.script import script_str, body_str
    # Detect the format, if not stated
    if datatype is None:
        if filename.endswith('.x3d'):
            datatype = 'X3D'
        elif filename.endswith('.html'):
            datatype = 'X3DOM'
        else:
            raise ValueError("filename must end in '.x3d' or '.html'.")
    # Write the header
    header = []
    if datatype == 'X3DOM':
        header.append('<html>\n')
        header.append('<head>\n')
        header.append('<title>ASE atomic visualization</title>\n')
        header.append('<link rel="stylesheet" type="text/css"\n')
        header.append(' href="https://www.x3dom.org/x3dom/release/x3dom.css">\n')
        header.append('</link>\n')
        header.append('<script type="text/javascript"\n')
        header.append(' src="https://www.x3dom.org/x3dom/release/x3dom.js">\n')
        header.append('</script>\n')
        header.extend(script_str)
        header.append('</head>\n')
        header.append('<body>\n')
        header.append(body_str)
        header.append('<X3D>\n')
        # header.append('<X3D width="400" height="400">\n')
    elif datatype == 'X3D':
        header.append(0, '<?xml version="1.0" encoding="UTF-8"?>\n')
        header.append(0, '<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.2//EN" '
            '"http://www.web3d.org/specifications/x3d-3.2.dtd">\n')
        header.append(0, '<X3D profile="Interchange" version="3.2" '
            'xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance" '
            'xsd:noNamespaceSchemaLocation='
            '"http://www.web3d.org/specifications/x3d-3.2.xsd">\n')
    else:
        raise ValueError("datatype not supported: " + str(datatype))
    #
    tail = []
    if datatype == 'X3DOM':
        tail.append('</X3D>\n')
        tail.append('</body>\n')
        tail.append('</html>\n')
    elif datatype == 'X3D':
        tail.append('</X3D>\n')
    return header, tail
#========================================================

if __name__ == "__main__":
    from ase.build import molecule
    atoms = molecule('H2O')
    atoms.center(3.0)
    # atoms = atoms*[5, 5, 5]
    atoms.pbc = [True, True, True]
    obj = X3D(atoms)
    obj.write('h2o.html', show_unit_cell = True)
