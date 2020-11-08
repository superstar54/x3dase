"""
Python module to view ASE atomic structures interactively using X3DOM.
"""

from x3dase.tools import get_atom_kinds, get_bond_kinds, get_polyhedra_kinds, build_tag, get_bondpairs
from x3dase.script import build_script, build_html, build_css, atoms2dict
import numpy as np
import uuid


def write_x3d(filename, atoms, format=None, **kwargs):
    """Writes to html using X3DOM.

    Args:
        filename - filename or output file object
        atoms - Atoms object to be rendered
        format - str, either 'X3DOM' for web-browser compatibility or 'X3D'
            to be readable by Blender. `None` to detect format based on file
            extension ('.html' -> 'X3DOM', '.x3d' -> 'X3D')"""
    obj = X3D(atoms, **kwargs)
    obj.write(filename, datatype=format)

class X3D:
    """
    """

    def __init__(self, images, quality = 'high', show_unit_cell = False, scale = 1.0, bond = False, rmbonds = {}, label = False, polyhedra = {}, isosurface = False, **kwargs):
        self.uuid = str(uuid.uuid4())[:8]
        if not isinstance(images, list):
            images = [images]
        self.images = images
        self.nimage = len(images)
        self._atoms = images[0].copy()
        self.natom = len(self._atoms)
        self.data = atoms2dict(self._atoms)
        self.data['uuid'] = '"%s"'%self.uuid
        self.data['label'] = '"%s"'%str(label)
        self.data['bond'] = '"%s"'%str(bond)
        self.data['polyhedra'] = '%s'%str(polyhedra)
        self.show_unit_cell = show_unit_cell
        self.bond = bond
        self.rmbonds = rmbonds
        self.label = label
        self.isosurface = isosurface
        self.polyhedra = polyhedra
        self.quality = quality
        self.atom_kinds = get_atom_kinds(self._atoms, scale = scale)
        self.com = self._atoms.get_center_of_mass()
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
        """
        """
        
        script = build_script(self.uuid, self.data)
        body = build_html(self.uuid)
        out, tail, datatype = write_header_tail(script, body, datatype, filename)
        #
        view_str = self.viewpoint()
        atomic_str = self.draw_atoms()
        cell_str = self.draw_cells()
        bond_str = self.draw_bonds()
        polyhedra_str = self.draw_polyhedras()
        iso_str = self.get_isosurface()
        marker_str = self.draw_marker()
        # animate
        ani_str = self.animate()
        scene_str = view_str + atomic_str + cell_str + bond_str + polyhedra_str + iso_str + marker_str + ani_str
        scene_str = build_tag('Scene', body = scene_str)
        
        if datatype == 'X3DOM':
            x3d_str = build_tag('X3D', id = "x3dase", PrimitiveQuality=self.quality, body = scene_str)
            x3d_str = build_tag('div', dict = {'class': 'column right'}, body = x3d_str)
        elif datatype == 'X3D':
            x3d_str = build_tag('X3D', body = scene_str, profile='Immersive', version='3.0',  
                                dict = {'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema-instance', 
                                        'xsd:noNamespaceSchemaLocation': ' http://www.web3d.org/specifications/x3d-3.0.xsd'})
        out.extend(x3d_str)
        out.extend(tail)
        if isinstance(filename, str):
            with open(filename, 'w') as f:
                for line in out:
                    f.write(line)
        else:
            f = filename
            for line in out:
                f.write(''.join(line))

    def viewpoint(self, ):
        view_str = ''
        com = self._atoms.get_center_of_mass()
        positions = self._atoms.positions
        R = max(max(positions[:, 0]) - min(positions[:, 0]), max(positions[:, 1]) - min(positions[:, 1]))
        camera_persp = build_tag('Viewpoint', id="camera_persp_%s"%self.uuid, position=tuple(com+[0, 0, 3*R]), centerOfRotation = tuple(com), orientation="0 0 0 0", description="camera")
        camera_persp  = build_tag('Transform', id = "t_camera_persp_%s"%self.uuid, rotation = '0 0 0 0', body = camera_persp)
        camera_ortho = build_tag('OrthoViewpoint', id="camera_ortho_%s"%self.uuid, position=tuple(com+[0, 0, 3*R]), centerOfRotation = tuple(com), orientation="0 0 0 0", fieldOfView='-{0} -{0} {0} {0}'.format(R), description="camera")
        camera_ortho  = build_tag('Transform', id = "t_camera_ortho_%s"%self.uuid, rotation = '0 0 0 0', body = camera_ortho)
        view_str = camera_persp + camera_ortho
        return view_str
    def draw_marker(self, ):
        marker_str = []
        # sphere
        for i in range(5):
            material = build_tag('Material', diffuseColor="#FFD966", transparency = 0.5)
            appearance = build_tag('Appearance', body=material)
            sphere = build_tag('Sphere', radius = 1.0)
            shape = build_tag('Shape', isPickable = False, body = appearance + sphere)
            trans = build_tag('Transform', id = 'marker_%s_%s'%(i, self.uuid), body = shape, scale=".1 .1 .1", translation="5 0 0")
            marker_str.extend(build_tag('Switch', id = 'switch_marker_%s_%s'%(i, self.uuid), body = trans, whichChoice = "-1"))
        # lines
        for i in range(2):
            coordIndex = '0 1 -1'
            point = '0 0 0 0 0 1'
            material = build_tag('Material', diffuseColor = (0, 0, 0), emissiveColor = (0, 0.5, 1))
            appearance = build_tag('Appearance', body = material)
            coord = build_tag('Coordinate', id = 'line_coor_%s_%s'%(i, self.uuid), point = point)
            line = build_tag('IndexedLineSet', id = 'line_ind_%s_%s'%(i, self.uuid), solid='false', coordIndex = coordIndex, body = coord)
            line = build_tag('Shape', body = line + appearance)
            marker_str.extend(build_tag('Switch', id = 'switch_line_%s_%s'%(i, self.uuid), body = line, whichChoice = "-1"))
        return marker_str
    def animate(self, ):
        '''
        <timeSensor DEF="time" cycleInterval="2" loop="true"> </timeSensor>
        <PositionInterpolator DEF="move" key="0 0.5 1" keyValue="0 0 0  0 3 0  0 0 0"> </PositionInterpolator>
        <Route fromNode="time" fromField ="fraction_changed" toNode="move" toField="set_fraction> </Route> 
        <Route fromNode="move" fromField ="value_changed" toNode="ball" toField="translation> </Route>  
        '''
        ani_str = []
        if self.nimage == 1: return ani_str
        ani_str.extend(build_tag('TimeSensor', DEF='time', cycleInterval = self.nimage, loop = 'true'))
        for i in range(len(self._atoms)):
            route1 = build_tag('ROUTE', fromNode='time', fromField='fraction_changed', toNode='move_%s'%i, toField='set_fraction')
            route2 = build_tag('ROUTE', fromNode="move_%s"%i, fromField ="value_changed", toNode="at_%s_%s"%(i, self.uuid), toField="translation")
            key = ""
            keyvalue = ""
            for j in range(self.nimage):
                key += " %s"%(j/self.nimage)
                keyvalue += '%s %s %s '%tuple(self.images[j][i].position)
            pi = build_tag('PositionInterpolator', DEF = 'move_%s'%i, key = key, keyValue = keyvalue)
            ani_str.extend(pi)
            ani_str.extend(route1)
            ani_str.extend(route2)
        return ani_str
    def draw_atoms(self):
        '''
        Draw atoms
        bsdf_inputs: dict
            The key and value for principled_bsdf node
        material_style: string
            Select materials type from ['blase', 'glass', 'ceramic', 'plastic'].
        '''
        # build materials
        atomic_str = []
        label_str = []
        group_ele = []
        group_ind = []
        for kind, datas in self.atom_kinds.items():
            material0 = build_tag('Material', name = 'am_%s'%self.uuid, **datas['material'])
            sphere0 = build_tag('Sphere', DEF = 'asp_%s'%kind, **datas['sphere'])
            appearance0 = build_tag('Appearance', DEF = 'app_%s'%kind, body=material0)
            shape0 = build_tag('Shape', DEF='as_%s'%kind, id = 'as_%s_%s'%(kind, self.uuid), body = appearance0 + sphere0)
            atomic_str.extend(build_tag('Switch', body = shape0, whichChoice = "-1"))
            # switch = build_tag('Switch', body = shape, whichChoice = "-1")
            material1 = build_tag('Material', diffuseColor = (0, 0, 0))
            appearance_text0 = build_tag('Appearance', DEF = 'text_app_%s'%kind, body=material1)
            fontstyle0 = build_tag('Fontstyle', DEF = 'st_label', family="SANS", size="%s"%(datas['sphere']['radius']/2.0)) #, justify='"MIDDLE", "MIDDLE"')
            label_str.extend(fontstyle0)
            label_str.extend(appearance_text0)
            # label_str.extend(switch)
            # element text
            ele = build_tag('Text', string = kind, solid = 'true', body = fontstyle0)
            shape_ele0 = build_tag('Shape', DEF=kind, id = 'as_%s'%self.uuid, body = appearance_text0 + ele)
            shape_ele0 = build_tag('Billboard', DEF = 'billboard_%s'%kind, axisOfRotation = (0 ,0 ,0), body = shape_ele0)
            label_str.extend(build_tag('Switch', body = shape_ele0, whichChoice = "-1"))
            iatom = 0
            for pos in datas['positions']:
                # atoms sphere
                sphere = build_tag('Sphere', USE='asp_%s'%kind)
                appearance = build_tag('Appearance', USE='app_%s'%kind)
                shape = build_tag('Shape', kind=kind, index = datas['indexs'][iatom], uuid = self.uuid, body = appearance + sphere)
                atomic_str.extend(build_tag('Transform', DEF ="at_%s_%s"%(datas['indexs'][iatom], self.uuid), uuid = self.uuid, id ="at_%s_%s"%(datas['indexs'][iatom], self.uuid), radius = datas['sphere']['radius'], name = "at_%s"%(self.uuid), body=shape, translation = tuple(pos), scale = "1 1 1"))
                # index
                appearance = build_tag('Appearance', USE = 'text_app_%s'%kind) #, justify='"MIDDLE", "MIDDLE"')
                ind = build_tag('Text', string = datas['indexs'][iatom], solid = 'true', body = fontstyle0)
                shape_ind = build_tag('Shape', body = appearance + ind)
                shape_ind = build_tag('Billboard', axisOfRotation = (0 ,0 ,0), body = shape_ind)
                group_ind.extend(build_tag('Transform', body=shape_ind, translation = tuple(pos)))
                # element text
                shape_ele = build_tag('Billboard', axisOfRotation = (0 ,0 ,0), USE='billboard_%s'%kind)
                group_ele.extend(build_tag('Transform', body=shape_ele, translation = tuple(pos)))
                iatom += 1
        atomic_str = build_tag('Group', body = atomic_str, onclick="handleGroupClick(event, '%s')"%self.uuid)
        if self.label:
            group_ele = build_tag('Group', body = group_ele)
            group_ind = build_tag('Group', body = group_ind)
            atomic_str.extend(label_str)
            atomic_str.extend(build_tag('Switch', id = "ele_%s"%self.uuid, body = group_ele, whichChoice = "-1"))
            atomic_str.extend(build_tag('Switch', id = "ind_%s"%self.uuid, body = group_ind, whichChoice = "-1"))
        return atomic_str
    def draw_cells(self, celllinewidth = 0.05):
        """
        Draw unit cell
        """
        cell_str = []
        if self.cell_vertices is not None:
            # edges
            coordIndex =      '0 1 -1 0 2 -1 0 4 -1 1 3 -1 1 5 -1 2 3 -1 2 6 -1 3 7 -1 4 5 -1 4 6 -1 5 7 -1 6 7 -1'
            # coordIndex = '0 1 2 3 0 -1 4 5 6 7 4 -1 0 4 -1 1 5 -1 2 6 -1 3 7'
            point = str(self.cell_vertices)
            # edge
            material = build_tag('Material', diffuseColor = (0, 0, 0), emissiveColor = (0, 0.5, 1))
            appearance = build_tag('Appearance', body = material)
            coord = build_tag('Coordinate', point = point)
            edge = build_tag('IndexedLineSet', coordIndex = coordIndex, body = coord)
            edge = build_tag('Shape', body = edge + appearance)
            cell_str.extend(edge)
        return cell_str

    def draw_bonds(self):
        '''
        Draw atom bonds
        '''
        # build materials
        bond_str = []
        if not self.bond:
            return bond_str
        bondlist = get_bondpairs(self._atoms, cutoff = self.bond, rmbonds = self.rmbonds)
        self.bond_kinds = get_bond_kinds(self._atoms, self.atom_kinds, bondlist)
        group = []
        for kind, datas in self.bond_kinds.items():
            material = build_tag('Material', **datas['material'])
            sphere = build_tag('Cylinder', height = 1.0, radius = 0.1, subdivision = 8)
            appearance = build_tag('Appearance', body=material)
            shape = build_tag('Shape', DEF=kind, body = appearance + sphere)
            switch = build_tag('Switch', body = shape, whichChoice = "-1")
            bond_str.extend(switch)
            for pos, height, rotation in zip(datas['centers'], datas['lengths'], datas['rotations']):
                shape1 = build_tag('Shape', USE=kind)
                bt = build_tag('Transform', body=shape1, translation = tuple(pos), scale = (1, height, 1), rotation = tuple(rotation))
                group.extend(bt)
        group = build_tag('Group', body = group)
        bond_str.extend(build_tag('Switch', id = "bs_%s"%self.uuid, body = group, whichChoice = "-1"))
        return bond_str
    def draw_polyhedras(self,):
        '''
        Draw polyhedras
        '''
        polyhedra_str = []
        if not self.polyhedra:
            return polyhedra_str
        bondlist = get_bondpairs(self._atoms, cutoff = self.bond, rmbonds=self.rmbonds)
        self.polyhedra_kinds = get_polyhedra_kinds(self._atoms, bondlist = bondlist, polyhedra = self.polyhedra)
        for kind, datas in self.polyhedra_kinds.items():
            material = build_tag('Material', **datas['material'], ambientIntensity = 0)
            appearance = build_tag('Appearance', body = material)
            facecoordIndex_str = ' '
            coordinate_str = ' '
            edgecoordIndex_str = ' '
            for face in datas['faces']:
                facecoordIndex_str += ' '.join(str(x) for x in face) + ' -1 '
            for coordinate in datas['vertices']:
                coordinate_str += ' '.join(str(x) for x in coordinate) + ' '
            for edge in datas['edges']:
                edgecoordIndex_str += ' '.join(str(x) for x in edge) + ' -1 '
            coord = build_tag('Coordinate', point = coordinate_str)
            # face
            face = build_tag('IndexedFaceSet', solid='false', coordIndex = facecoordIndex_str, body = coord)
            polyhedra_str.extend(build_tag('Shape', body = face + appearance))
            # edge
            material = build_tag('Material', diffuseColor = (1, 1, 1), emissiveColor = (0.8, 0.8, 0.8), ambientIntensity = 0)
            appearance = build_tag('Appearance', body = material)
            edge = build_tag('IndexedLineSet', coordIndex = edgecoordIndex_str, body = coord)
            polyhedra_str.extend(build_tag('Shape', body = edge + appearance))
        polyhedra_str = build_tag('Group', body = polyhedra_str)
        polyhedra_str = (build_tag('Switch', id = "ps_%s"%self.uuid, body = polyhedra_str, whichChoice = "-1"))
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
        iso_str = []
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
            iso_str.extend(self.draw_isosurface(np.round(scaled_verts, decimals = 3), faces, color = colors[icolor]))
            icolor += 1
        return iso_str
    def draw_isosurface(self, vertices, faces, color):
        """ 
        """
        iso_str = []
        material = build_tag('Material', diffuseColor = color, transparency = 0.4)
        appearance = build_tag('Appearance', body = material)
        facecoordIndex_str = ' '
        coordinate_str = ' '
        for face in faces:
            facecoordIndex_str += ' '.join(str(x) for x in face) + ' -1 '
        for coordinate in vertices:
            coordinate_str += ' '.join(str(x) for x in coordinate) + ' '
        coord = build_tag('Coordinate', point = coordinate_str)
        face = build_tag('IndexedFaceSet', solid='false', coordIndex = facecoordIndex_str, body = coord)
        face = build_tag('Shape', body = face + appearance)
        iso_str.extend(face)
        iso_str = build_tag('Group', onclick="handleGroupClick(event)", body = iso_str)
        return iso_str

def write_header_tail(script, body, datatype, filename):
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
        header.append(build_css())
        header.append('</head>\n')
        header.append('<body>\n')
        header.append(body)
    elif datatype == 'X3D':
        header.append('<?xml version="1.0" encoding="UTF-8"?>\n')
        header.append('<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.2//EN" '
            '"http://www.web3d.org/specifications/x3d-3.2.dtd">\n')
    else:
        raise ValueError("datatype not supported: " + str(datatype))
    #
    tail = []
    if datatype == 'X3DOM':
        tail.append(script)
        tail.append('</body>\n')
        tail.append('</html>\n')
    return header, tail, datatype


#========================================================

if __name__ == "__main__":
    from ase.build import molecule, fcc111
    from ase.io import read
    from x3dase.x3d import X3D
    from ase.io import read, write
    atoms = molecule('H2O')
    X3D(atoms, bond = 1.0).write('h2o.html')
    atoms = fcc111('Pt', size = (20, 20, 4), vacuum=5.0)
    X3D(atoms).write('pt.html')
    # images = read('examples/datas/ti-56-63.xyz', index = ':')
    # X3D(images[0], bond = 1.0, rmbonds = {'Ti':['Ti', 'La'], 'La':['La', 'O', 'N']}, label = True, polyhedra = {'Ti':['O', 'N']}).write('c2h6so-ani.html')