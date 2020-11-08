import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="x3dase",
    version="1.1.3",
    description="Drawing and rendering atoms and molecules objects using X3DOM. X3dase can be used as a viewer for the molecule structure in the Jupyter notebook.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/superstar54/x3dase",
    author="Xing Wang",
    author_email="xingwang1991@gmail.com",
    license="GPL",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["x3dase"],
    #include_package_data=True,
    package_data = {
    'x3dase': ['html/menu.html', 'css/style.css', 'js/script.js', 'images/*png'],
    },
    install_requires=["ase", "numpy", "scipy"],
    python_requires='>=3',
)
