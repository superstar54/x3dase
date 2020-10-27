"""
Output support for X3D and X3DOM file types.
See http://www.web3d.org/x3d/specifications/
X3DOM outputs to html pages that should display 3-d manipulatable atoms in
modern web browsers.
"""

from ase.data import covalent_radii
from ase.data.colors import jmol_colors
import numpy as np
from x3dase.tools import get_atom_kinds, get_bond_kinds, get_polyhedra_kinds, build_tag, get_bondpairs
import time
import uuid


def write_x3d(filename, atoms, format=None, **kwargs):
    """Writes to html using X3DOM.

    Args:
        filename - str or file-like object, filename or output file object
        atoms - Atoms object to be rendered
        format - str, either 'X3DOM' for web-browser compatibility or 'X3D'
            to be readable by Blender. `None` to detect format based on file
            extension ('.html' -> 'X3DOM', '.x3d' -> 'X3D')"""
    X3D(atoms, **kwargs).write(filename, datatype=format)


def write_html(filename, atoms, **kwargs):
    """Writes to html using X3DOM

    Args:
        filename - str or file-like object, filename or output file object
        atoms - Atoms object to be rendered"""
    write_x3d(filename, atoms, format='X3DOM', **kwargs)


class X3D:
    """Class to write either X3D (readable by open-source rendering
    programs such as Blender) or X3DOM html, readable by modern web
    browsers.
    """

    def __init__(self, atoms, show_unit_cell = None, scale = 1.0, bond = None, polyhedra_dict = {}, isosurface = None, **kwargs):
        self._atoms = atoms
        self.show_unit_cell = show_unit_cell
        self.bond = bond
        self.isosurface = isosurface
        self.polyhedra_dict = polyhedra_dict
        self.atom_kinds = get_atom_kinds(atoms, scale = scale)
        self.uuid = str(uuid.uuid1()).replace('-', '_')
        #
        if self._atoms.pbc.any():
            cell = self._atoms.cell
            cell_vertices = np.empty((2, 2, 2, 3))
            for c1 in range(2):
                for c2 in range(2):
                    for c3 in range(2):
                        cell_vertices[c1, c2, c3] = np.dot([c1, c2, c3],
                                                            cell)
            cell_vertices.shape = (1, 24)
            self.cell_vertices = cell_vertices
        else:
            self.cell_vertices = None
            
        

    def write(self, filename, datatype=None, **kwargs):
        """Writes output to either an 'X3D' or an 'X3DOM' file, based on
        the extension. For X3D, filename should end in '.x3d'. For X3DOM,
        filename should end in '.html'.

        Args:
            filename - str or file-like object, output file name or writer
            datatype - str, output format. 'X3D' or 'X3DOM'. If `None`, format
                will be determined from the filename"""

        out, tail = write_header_tail(self.uuid, datatype, filename)
        out.append('<Scene>\n')
        atomic_str = self.draw_atoms()
        out.extend(atomic_str)
        cell_str = self.draw_cells()
        out.extend(cell_str)
        bond_str = self.draw_bonds()
        out.extend(bond_str)
        polyhedra_str = self.draw_polyhedras()
        out.extend(polyhedra_str)
        iso_str = self.get_isosurface()
        out.extend(iso_str)
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
            material = build_tag('Material', name = 'am_%s'%self.uuid, **datas['material'])
            sphere = build_tag('Sphere', **datas['sphere'])
            appearance = build_tag('Appearance', body=material)
            # switch = build_tag('Switch', body = shape, whichChoice = "-1")
            material1 = build_tag('Material', diffuseColor = (0, 0, 0))
            appearance1 = build_tag('Appearance', body=material1)
            screenfontstyle = build_tag('fontstyle', family="SANS", size="%s"%datas['sphere']['radius']) #, justify='"MIDDLE", "MIDDLE"')
            # atomic_str += switch
            i = 0
            for pos in datas['positions']:
                pos1 = pos + np.array([0, 0, 0.0])
                shape = build_tag('Shape', DEF=kind, id = self.uuid, body = appearance + sphere)
                # index
                ind = build_tag('Text', string = datas['indexs'][i], solid = 'true', body = screenfontstyle)
                shape_ind = build_tag('Shape', DEF=kind, id = self.uuid, body = appearance1 + ind)
                shape_ind = build_tag('Billboard', axisOfRotation = (0 ,0 ,0), body = shape_ind)
                shape_ind = build_tag('Transform', id = self.uuid, body=shape_ind, translation = tuple(pos1))
                # element
                ele = build_tag('Text', string = kind, solid = 'true', body = screenfontstyle)
                shape_ele = build_tag('Shape', DEF=kind, id = self.uuid, body = appearance1 + ele)
                shape_ele = build_tag('Billboard', axisOfRotation = (0 ,0 ,0), body = shape_ele)
                shape_ele = build_tag('Transform', id = self.uuid, body=shape_ele, translation = tuple(pos1))
                #
                atomic_str += build_tag('Transform', id = self.uuid, name = "at_%s"%self.uuid, body=shape, translation = tuple(pos))
                atomic_str += build_tag('Switch', name = "ind_%s"%self.uuid, body = shape_ind, whichChoice = "-1")
                atomic_str += build_tag('Switch', name = "ele_%s"%self.uuid, body = shape_ele, whichChoice = "-1")
                i += 1
            # print('atoms: {0}   {1:10.2f} s'.format(kind, time.time() - tstart))
        # atomic_str = build_tag('Group', onclick="handleGroupClick_{0}(event)".format(self.uuid), body = atomic_str)
        atomic_str = build_tag('Group', body = atomic_str)
        return atomic_str
    def draw_cells(self, celllinewidth = 0.05):
        """
        Draw unit cell
        """
        cell_str = ''
        if self.cell_vertices is not None:
            # edges
            coordIndex =      '0 1 -1 0 2 -1 0 4 -1 1 3 -1 1 5 -1 2 3 -1 2 6 -1 3 7 -1 4 5 -1 4 6 -1 5 7 -1 6 7 -1'
            # coordIndex = '0 1 2 3 0 -1 4 5 6 7 4 -1 0 4 -1 1 5 -1 2 6 -1 3 7'
            point = str(self.cell_vertices)
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
        if not self.bond:
            return bond_str
        bondlist = get_bondpairs(self._atoms, cutoff = self.bond)
        self.bond_kinds = get_bond_kinds(self._atoms, self.atom_kinds, bondlist)
        for kind, datas in self.bond_kinds.items():
            tstart = time.time()
            material = build_tag('Material', **datas['material'])
            sphere = build_tag('Cylinder', height = 1.0, radius = 0.1)
            appearance = build_tag('Appearance', body=material)
            shape = build_tag('Shape', DEF=kind, body = appearance + sphere)
            switch = build_tag('Switch', body = shape, whichChoice = "-1")
            bond_str += switch
            for pos, height, rotation in zip(datas['centers'], datas['lengths'], datas['rotations']):
                shape1 = build_tag('Shape', USE=kind)
                bt = build_tag('Transform', body=shape1, translation = tuple(pos), scale = (1, height, 1), rotation = rotation)
                bond_str += build_tag('Switch', name = "bs_%s"%self.uuid, body = bt, whichChoice = "0")
            # print('bond: {0}   {1:10.2f} s'.format(kind, time.time() - tstart))
        # bond_str = build_tag('Switch', id = "bs_%s"%self.uuid, body = bond_str, whichChoice = "0")
        return bond_str
    def draw_polyhedras(self,):
        '''
        Draw polyhedras
        '''
        polyhedra_str = ''
        if not self.polyhedra_dict:
            return polyhedra_str
        bondlist = get_bondpairs(self._atoms, cutoff = self.bond)
        self.polyhedra_kinds = get_polyhedra_kinds(self._atoms, bondlist = bondlist, polyhedra_dict = self.polyhedra_dict)
        for kind, datas in self.polyhedra_kinds.items():
            tstart = time.time()
            material = build_tag('Material', **datas['material'])
            facecoordIndex_str = ' '
            coordinate_str = ' '
            edgecoordIndex_str = ' '
            for face in datas['faces']:
                facecoordIndex_str += ' '.join(str(x) for x in face) + ' -1 '
            for coordinate in datas['vertices']:
                coordinate_str += ' '.join(str(x) for x in coordinate) + ' '
            for edge in datas['edges']:
                edgecoordIndex_str += ' '.join(str(x) for x in edge) + ' -1 '
            face = '''
            <Shape>
                <IndexedFaceSet solid='false' coordIndex="%s">
                    <Coordinate point="%s"/>
                </IndexedFaceSet>
                <Appearance>
                    %s
                </Appearance>
            </Shape>
            '''%(facecoordIndex_str, coordinate_str, material)
            edge = '''
            <Shape>
                <LineSet vertexCount="%s">
                    <Coordinate point="%s"/>
                </IndexedFaceSet>
                <Appearance>
                    %s
                </Appearance>
            </Shape>
            '''%(edgecoordIndex_str, coordinate_str, material)
            polyhedra_str += build_tag('Switch', name = "ps_%s"%self.uuid, body = face + edge, whichChoice = "0")
            # print('polyhedra: {0}   {1:10.2f} s'.format(kind, time.time() - tstart))
        polyhedra_str = build_tag('Group', onclick="handleGroupClick(event)", body = polyhedra_str)
        return polyhedra_str
    def get_isosurface(self, volume = None, level = 0.02,
                    closed_edges = False, gradient_direction = 'descent',
                    color=(0.85, 0.80, 0.25) , icolor = None, transmit=0.5,
                    verbose = False, step_size = 1, ):
        '''
        Computes an isosurface from a volume grid.
        Parameters:    
          'isosurface': [data, -0.002, 0.002],
        '''
        from skimage import measure
        iso_str = ' '
        if not self.isosurface: return iso_str
        colors = [(0.85, 0.80, 0.25), (0.0, 0.0, 1.0)]
        volume = self.isosurface[0]
        cell = self._atoms.cell
        cell_vertices = self.cell_vertices
        cell_vertices.shape = (2, 2, 2, 3)
        cell_origin = cell_vertices[0,0,0]
        #
        spacing = tuple(1.0/np.array(volume.shape))
        icolor = 0
        for level in self.isosurface[1:]:
            scaled_verts, faces, normals, values = measure.marching_cubes_lewiner(volume, level = level,
                        spacing=spacing,gradient_direction=gradient_direction , 
                        allow_degenerate = False, step_size=step_size)
            scaled_verts = list(scaled_verts)
            nverts = len(scaled_verts)
            # transform
            for i in range(nverts):
                scaled_verts[i] = scaled_verts[i].dot(cell)
                scaled_verts[i] -= cell_origin
            faces = list(faces)
            # print('Draw isosurface...')
            iso_str += self.draw_isosurface(scaled_verts, faces, color = colors[icolor])
            icolor += 1
        return iso_str
    def draw_isosurface(self, vertices, faces, color):
        """ 
        """
        iso_str = ''
        tstart = time.time()
        material = build_tag('Material', diffuseColor = color, transparency = 0.2)
        facecoordIndex_str = ' '
        coordinate_str = ' '
        for face in faces:
            facecoordIndex_str += ' '.join(str(x) for x in face) + ' -1 '
        for coordinate in vertices:
            coordinate_str += ' '.join(str(x) for x in coordinate) + ' '
        face = '''
        <Shape>
            <IndexedFaceSet solid='false' coordIndex="%s">
                <Coordinate point="%s"/>
            </IndexedFaceSet>
            <Appearance>
                %s
            </Appearance>
        </Shape>
        '''%(facecoordIndex_str, coordinate_str, material)
        iso_str += face
        # print('polyhedra: {0}   {1:10.2f} s'.format(kind, time.time() - tstart))
        iso_str = build_tag('Group', onclick="handleGroupClick(event)", body = iso_str)
        return iso_str

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



def write_header_tail(uuid, datatype, filename):
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
        header.append('</head>\n')
        header.append('<body>\n')
        header.append(body_str(uuid))
        # header.append('<X3D>\n')
        header.append('<X3D width="80%" height="80%">\n')
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
        tail.extend(script_str(uuid))
        tail.append('</body>\n')
        tail.append('</html>\n')
    elif datatype == 'X3D':
        tail.append('</X3D>\n')
    return header, tail
#========================================================

if __name__ == "__main__":
    from ase.build import molecule
    from x3dase.x3d import X3D
    from ase.io import read, write
    from x3dase.x3d import write_html
    atoms = molecule('C2H6SO')
    X3D(atoms, bond = 1.0).write('c2h6so.html')
    atoms = molecule('H2O')
    X3D(atoms, bond = 1.0).write('h2o.html')
    atoms = read('examples/datas/perovskite.cif')
    atoms.pbc = [True, True, True]
    atoms = atoms*[2, 2, 2]
    write_html('perovskite.html', atoms, show_unit_cell = True, bond = 1.0, polyhedra_dict =  {'Pb': ['I']})
