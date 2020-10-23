"""Inline viewer for jupyter notebook using X3D."""

from x3dase.x3d import write_html
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from IPython.display import HTML

def view_x3d(atoms, **kwargs):
    """View atoms inline in a jupyter notbook. This command
    should only be used within a jupyter/ipython notebook.
    
    Args:
        atoms - ase.Atoms, atoms to be rendered"""
    
    output = StringIO()
    write_html(output, atoms, **kwargs)
    data = output.getvalue()
    output.close()
    return HTML(data)
