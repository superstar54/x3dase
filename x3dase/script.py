'''
'''
import pathlib
import os
cwd = pathlib.Path(__file__).parent.absolute()

def atoms2dict(atoms):
    com = atoms.get_center_of_mass()
    positions = atoms.positions
    R = max(max(positions[:, 0]) - min(positions[:, 0]), max(positions[:, 1]) - min(positions[:, 1]))
    data = {
        'com': "{0:1.2f} {1:1.2f} {2:1.2f}".format(com[0], com[1], com[2]),
        'top_pos': "{0:1.2f} {1:1.2f} {2:1.2f}".format(com[0], com[1], com[2] + 3*R),
        'front_pos': "{0:1.2f} {1:1.2f} {2:1.2f}".format(com[0], com[1] - 3*R, com[2]),
        'right_pos': "{0:1.2f} {1:1.2f} {2:1.2f}".format(com[0] + 3*R, com[1], com[2]),
        'left_pos': "{0:1.2f} {1:1.2f} {2:1.2f}".format(com[0]  - 3*R, com[1], com[2]),
    }
    
    return data
def pytojs_dict(data, uuid):
    atoms_dict = 'let atoms_dict = {'
    for key, value in data.items():
        atoms_dict += '%s: "%s", \n'%(key, value)
    atoms_dict += '}'
    return atoms_dict

def build_css():
    css_str = '<style>'
    with open(os.path.join(cwd, 'style.css'), 'r') as f:
        css = f.read()
    css_str += css
    css_str += '</style>'
    return css_str

def build_script(uuid, data):
    mystr = """
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.0.min.js" ></script>
 <script >\n"""
    mystr += pytojs_dict(data, uuid)
    with open(os.path.join(cwd, 'script.js'), 'r') as f:
        script = f.read()
    # mystr += script.replace('uuid', "'%s'"%uuid)
    mystr += script
    mystr += '</script> '
    return mystr

def build_body(uuid, data):
    body_str = '''
<div class = "column left", id = "sidebar">

<p>Models: <br>
<button type="button" onclick="spacefilling('{0}')">Space-filling</button>
<button type="button" onclick="ballstick('{0}')">Ball-and-stick</button>
<button type="button" onclick="polyhedra('{0}')">Polyhedra</button>   
<br>
Labels: <br>
<button type="button" onclick="none('{0}')">None</button>
<button type="button" onclick="element('{0}')"> Element</button>
<button type="button" onclick="index('{0}')">Index</button>

<div id="camera_buttons" style="display: block;">
<br>
Camera:<br>
    <button onclick="document.getElementById('camera_ortho_{0}').setAttribute('set_bind','true');">Orthographic <br></button>
    <button onclick="document.getElementById('camera_persp_{0}').setAttribute('set_bind','true');">Perspective <br></button>
<br>
View:<br>
    <button  onclick="set_viewpoint('{0}', 'top')">Top<br></button>
    <button  onclick="set_viewpoint('{0}', 'front')">Front<br></button>
    <button  onclick="set_viewpoint('{0}', 'right')">Right<br></button>
    <button onclick="set_viewpoint('{0}', 'left')">Left <br></button>
</div>

</p>
    <table style="font-size:1.0em;">
        <tr><td>Element: </td><td id="lastonMouseoverObject_kind_{0}">-</td> <td> <td id="lastonMouseoverObject_index_{0}">-</td> <td>  </td><td id="position_{0}">-</td></tr>
    </table>
<p id="distance_{0}"></p>
<p id="error_{0}"></p>

</div>
'''.format(uuid)
    return body_str



if __name__ == "__main__":
    from ase.build import molecule
    atoms = molecule('H2O')
    data = atoms2dict(atoms)
    mystr = build_script('1ad', data)
    print(mystr)