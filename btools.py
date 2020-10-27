import numpy as np
from scipy.spatial.transform import Rotation as R
import time
######################################################


    
def draw_polyhedras(bobj, coll = None, polyhedra_kinds = None, polyhedra_dict= None, bsdf_inputs = None, material_style = 'plastic'):
    '''
    Draw polyhedras
    '''
    if not  coll:
        coll = bobj.coll
    coll_polyhedra_kinds = [c for c in coll.children if 'polyhedras' in c.name][0]
    if not polyhedra_kinds:
        polyhedra_kinds = bobj.polyhedra_kinds
    if not bsdf_inputs:
        bsdf_inputs = bobj.material_styles_dict[material_style]
    #
    
    # import pprint
    # pprint.pprint(polyhedra_kinds)
    source = bond_source(vertices=4)
    for kind, datas in polyhedra_kinds.items():
        tstart = time.time()
        material = bpy.data.materials.new('polyhedra_kind_{0}'.format(kind))
        material.diffuse_color = np.append(datas['color'], datas['transmit'])
        # material.blend_method = 'BLEND'
        material.use_nodes = True
        principled_node = material.node_tree.nodes['Principled BSDF']
        principled_node.inputs['Base Color'].default_value = np.append(datas['color'], datas['transmit'])
        principled_node.inputs['Alpha'].default_value = polyhedra_kinds[kind]['transmit']
        for key, value in bsdf_inputs.items():
            principled_node.inputs[key].default_value = value
        datas['materials'] = material
        #
        # create new mesh structure
        mesh = bpy.data.meshes.new("mesh_kind_{0}".format(kind))
        # mesh.from_pydata(polyhedra_kinds[kind]['vertices'], polyhedra_kinds[kind]['edges'], polyhedra_kinds[kind]['faces'])  
        mesh.from_pydata(datas['vertices'], [], datas['faces'])  
        mesh.update()
        for f in mesh.polygons:
            f.use_smooth = True
        obj_polyhedra = bpy.data.objects.new("polyhedra_kind_{0}".format(kind), mesh)
        obj_polyhedra.data = mesh
        obj_polyhedra.data.materials.append(material)
        bpy.ops.object.shade_smooth()
        #---------------------------------------------------
        material = bpy.data.materials.new('polyhedra_edge_kind_{0}'.format(kind))
        material.diffuse_color = np.append(datas['edge_cylinder']['color'], datas['edge_cylinder']['transmit'])
        # material.blend_method = 'BLEND'
        material.use_nodes = True
        principled_node = material.node_tree.nodes['Principled BSDF']
        principled_node.inputs['Base Color'].default_value = np.append(datas['edge_cylinder']['color'], datas['edge_cylinder']['transmit'])
        principled_node.inputs['Alpha'].default_value = datas['transmit']
        for key, value in bsdf_inputs.items():
            principled_node.inputs[key].default_value = value
        datas['edge_cylinder']['materials'] = material
        verts, faces = cylinder_mesh_from_instance(datas['edge_cylinder']['centers'], datas['edge_cylinder']['normals'], datas['edge_cylinder']['lengths'], 0.01, source)
        # print(verts)
        mesh = bpy.data.meshes.new("mesh_kind_{0}".format(kind))
        mesh.from_pydata(verts, [], faces)  
        mesh.update()
        for f in mesh.polygons:
            f.use_smooth = True
        obj_edge = bpy.data.objects.new("edge_kind_{0}".format(kind), mesh)
        obj_edge.data = mesh
        obj_edge.data.materials.append(material)
        bpy.ops.object.shade_smooth()
        # STRUCTURE.append(obj_polyhedra)
        coll_polyhedra_kinds.objects.link(obj_polyhedra)
        coll_polyhedra_kinds.objects.link(obj_edge)
        print('polyhedras: {0}   {1:10.2f} s'.format(kind, time.time() - tstart))

def draw_isosurface(bobj = None, coll = None, volume = None, level = 0.02,
                    closed_edges = False, gradient_direction = 'descent',
                    color=(0.85, 0.80, 0.25) , icolor = None, transmit=0.5,
                    verbose = False, step_size = 1, 
                    bsdf_inputs = None, material_style = 'blase'):
    """Computes an isosurface from a volume grid.
    
    Parameters:     
    """
    from skimage import measure
    colors = [(0.85, 0.80, 0.25), (0.0, 0.0, 1.0)]
    if icolor:
        color = colors[icolor]
    if not  coll:
        coll = bobj.coll
    coll_isosurface = [c for c in coll.children if 'isosurfaces' in c.name][0]
    
    cell = bobj.cell
    bobj.cell_vertices.shape = (2, 2, 2, 3)
    cell_origin = bobj.cell_vertices[0,0,0]
    #
    spacing = tuple(1.0/np.array(volume.shape))
    scaled_verts, faces, normals, values = measure.marching_cubes_lewiner(volume, level = level,
                    spacing=spacing,gradient_direction=gradient_direction , 
                    allow_degenerate = False, step_size=step_size)
    #
    scaled_verts = list(scaled_verts)
    nverts = len(scaled_verts)
    # transform
    for i in range(nverts):
        scaled_verts[i] = scaled_verts[i].dot(cell)
        scaled_verts[i] -= cell_origin
    faces = list(faces)
    print('Draw isosurface...')
    # print('verts: ', scaled_verts[0:5])
    # print('faces: ', faces[0:5])
    #material
    if not bsdf_inputs:
        bsdf_inputs = bobj.material_styles_dict[material_style]
    material = bpy.data.materials.new('isosurface')
    material.name = 'isosurface'
    material.diffuse_color = color + (transmit,)
    # material.alpha_threshold = 0.2
    # material.blend_method = 'BLEND'
    material.use_nodes = True
    principled_node = material.node_tree.nodes['Principled BSDF']
    principled_node.inputs['Base Color'].default_value = color + (transmit,)
    principled_node.inputs['Alpha'].default_value = transmit
    for key, value in bsdf_inputs.items():
            principled_node.inputs[key].default_value = value
    #
    # create new mesh structure
    isosurface = bpy.data.meshes.new("isosurface")
    isosurface.from_pydata(scaled_verts, [], faces)  
    isosurface.update()
    for f in isosurface.polygons:
        f.use_smooth = True
    iso_object = bpy.data.objects.new("isosurface", isosurface)
    iso_object.data = isosurface
    iso_object.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    coll_isosurface.objects.link(iso_object)
