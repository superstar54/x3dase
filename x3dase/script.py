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
        'com': '"{0:1.2f} {1:1.2f} {2:1.2f}"'.format(com[0], com[1], com[2]),
        'top_pos': '"{0:1.2f} {1:1.2f} {2:1.2f}"'.format(com[0], com[1], com[2] + 3*R),
        'front_pos': '"{0:1.2f} {1:1.2f} {2:1.2f}"'.format(com[0], com[1] - 3*R, com[2]),
        'right_pos': '"{0:1.2f} {1:1.2f} {2:1.2f}"'.format(com[0] + 3*R, com[1], com[2]),
        'left_pos': '"{0:1.2f} {1:1.2f} {2:1.2f}"'.format(com[0]  - 3*R, com[1], com[2]),
        'top_ori': '"0 0 0 0"',
        'front_ori': '"1 0 0 1.57079"',
        'right_ori': '"0 1 0 1.57079"',
        'left_ori': '"0 1 0 -1.57079"',
        'select': '[]',
    }
    return data
def pytojs_dict(data, uuid):
    atoms_dict = 'if (atoms_dict == undefined) {var atoms_dict = {"new": true};}; \n'
    atoms_dict += 'atoms_dict["%s"] = {'%uuid
    for key, value in data.items():
        atoms_dict += '%s: %s, \n'%(key, value)
    atoms_dict += '};\n'
    # print(atoms_dict)
    return atoms_dict

def build_css():
    css_str = '<style>'
    with open(os.path.join(cwd, 'css/style.css'), 'r') as f:
        css = f.read()
    css_str += css
    css_str += '</style>'
    return css_str

def build_script(uuid, data):
    mystr = """
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.0.min.js" ></script>
 <script >\n """
    mystr += pytojs_dict(data, uuid)
    with open(os.path.join(cwd, 'js/script.js'), 'r') as f:
        script = f.read()
    mystr += script
    mystr += ' \n</script> '
    return mystr

def build_html(uuid):
    with open(os.path.join(cwd, 'html/menu.html'), 'r') as f:
        menu = f.read()
    html = menu
    html = html.replace('uuid', uuid)
    return html

if __name__ == "__main__":
    from ase.build import molecule
    atoms = molecule('H2O')
    data = atoms2dict(atoms)
    mystr = build_script('1ad', data)
    print(mystr)