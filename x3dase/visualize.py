"""Inline viewer for jupyter notebook using X3D."""

from x3dase.x3d import write_x3d
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from IPython.display import HTML
from IPython.display import IFrame

def view_x3d(atoms, **kwargs):
    """View atoms inline in a jupyter notbook.
    
    Parameters:
        atoms:
            ase.Atoms, atoms to be rendered.
        kwargs:
            all other parameters including bond, labels and so on.
    """
    
    output = StringIO()
    write_x3d(output, atoms, **kwargs)
    data = output.getvalue()
    output.close()
    return HTML(data)
def view_x3d_n(atoms, output = 'x3dase.html', **kwargs):
    """
    HTML <iframe> specifies an inline frame.
    Creat a html file, and display the web page within jupyter notebook.
    
    Parameters:
        atoms:
                ase.Atoms, atoms to be rendered.
        output:
                file name of the html file.
        """
    write_x3d(output, atoms, **kwargs)
    return IFrame(output, '1000px', '500px')

