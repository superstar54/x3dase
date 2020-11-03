# x3dase

Python module for drawing and rendering atoms and molecules objects using X3DOM. X3dase can be used as a viewer for the molecule structure in the Jupyter notebook.

Functions:
* Support all file-formats using by ASE, including cif, xyz, cube, pdb, json, VASP-out and so on.
* Ball & stick
* Space filling
* Polyhedral
* Isosurface
* Show element and index

For the introduction of ASE , please visit https://wiki.fysik.dtu.dk/ase/index.html


### Author
* Xing Wang  <xingwang1991@gmail.com>

### Dependencies

* Python
* ASE
* Skimage

### Installation

Clone this repo. Add it to your PYTHONPATH and PATH. On windows, you can edit the system environment variables.

``` sh
export PYTHONPATH=/path-to-x3dase:$PYTHONPATH
```

### Examples

#### Draw molecule in Jupyter notebooks

<img src="examples/images/jupyter.png" width="600"/>



#### Show different models
<img src="examples/images/models.png" width="500"/>


#### Polyhedra for crystal
<img src="examples/images/polyhedra.png" width="300"/>


#### Isosurface for electron density
<img src="examples/images/isosurface.png" width="300"/>
