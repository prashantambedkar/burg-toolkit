# BURG toolkit

This is a Python toolkit for **B**enchmarking and **U**nderstanding **R**obotic **G**rasping, developed 
in the scope of [BURG project](#references). Features are:
- core data structures for object types and instances, scenes, grippers, grasps and grasp sets
- antipodal grasp sampling
- physics simulation with pybullet
- depth/point cloud rendering with pybullet and/or pyrender
- metrics for evaluation of grasps and grasp sets
- visualization of scenes and grasps using open3d
- dataset creation

It is the backend to the [BURG Setup Tool](https://github.com/markus-suchi/burg-toolkit-gui).

## project structure

The project contains the following directories:
- **burg_toolkit** - the core Python library
- **scripts** - examples
- **tests** - messy manual, test files
- **docs** - configuration files to create documentation with sphinx
- **data** - simple data samples to be used in some example scripts

## installation

Developed for:
- Python 3.6-3.8
- Ubuntu 20.04 and Windows, but at some point we stopped testing on Windows

Recommended way is to install in a virtual environment.
Go inside project main directory (where the `setup.py` resides) and execute:

```
git clone git@github.com:mrudorfer/burg-toolkit.git
cd burg-toolkit

# create virtual environment
python3 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
pip install --upgrade setuptools wheel

# install burg_toolkit in editable mode, also see install options
pip install -e .
```
If you experience any problems, please open an issue.

Sometimes, especially if numpy has already been installed in the environment, there may be a mismatch of compiler versions which cause numpy-quaternion to fail. See https://github.com/moble/quaternion/issues/72 for details.

### install options

There are some dependencies not included in the default installation.
These are mostly packages that are either not required for regular usage or not installing smoothly on all platforms.
The following extras are available (general installation procedure as above, explanation in the subsequent sections):
```
pip install -e .['docs']  # includes packages required to build documentation
pip install -e .['collision']  # mesh-mesh collision checks
pip install -e .['openexr']  # read/write .exr image files
pip install -e .['full']  # install all optional dependencies
```

#### docs

Dependencies for the documentation should install smoothly on all platforms.
You can build the documentation on the command line (with virtual environment activated) via:

```
sphinx-apidoc -f -o docs burg_toolkit
cd docs/
make html  # linux
./make.bat html  # windows
```

The docs can then be found in `docs/_build/html`folder.


#### collision

Mesh-mesh collisions currently rely on `python-fcl` which is only available for linux.
There are some efforts to bring `python-fcl` to Windows, e.g. there are packages like
`python-fcl-win32` and `python-fcl-win32-nr`, but there seem to be issues installing those, see:
 https://github.com/BerkeleyAutomation/python-fcl/issues/17.
So far I have not been able to install either of those packages with `pip`.

#### openexr

This is required for saving images to `.exr` file format specified by OpenEXR.
It requires to install OpenEXR on your system.
On Linux, you can `sudo apt-get install libopenexr-dev` upon which the package should install smoothly.
On Windows, it is more complicated.
See https://stackoverflow.com/a/68102521/1264582.

## usage

Example:

```
import numpy as np
import burg_toolkit as burg

gs1 = burg.GraspSet.from_translations(np.random.random(50, 3))
gs2 = burg.GraspSet.from_translations(np.random.random(30, 3))
print('grasp coverage is:', burg.metrics.coverage(gs1, gs2))
```

See the scripts for more examples on usage and the docs for more detailed specifications.


## plans for the project

### house keeping

- replace messy manual test files with more reasonable unit testing
- properly load textures for meshes
- proper packaging/distribution of example files
- resolve numpy-quaternion issues in installation
- package-level logging
- update to newer open3d version
- documentation on readthedocs

### features
- grasp sampling
    - there is some unused code currently, needs better structure
    - more configurable AGS, e.g. with option to use random rotation offset for creating grasp orientations
    - more consistency in grasp representations, i.e. canonical forms, opening width, grasping depth, contact points etc.
    - computation of analytic success metrics
- simulation-based grasp assessment using pybullet
    - determine simulation-based grasp success rate for grasp sets
    - use various grippers
    
## Acknowledgments

The BURG research project is funded by CHIST-ERA and EPSRC.

## References

- BURG research project: https://burg.acin.tuwien.ac.at/
- Clemens Eppner, Arsalan Mousavian and Dieter Fox: "A Billion Ways to Grasps - An Evaluation of Grasp Sampling Schemes on a Dense, Physics-based Grasp Data Set", ISRR 2019 - https://sites.google.com/view/abillionwaystograsp
- Qian-Yi Zhou, Jaesik Park, and Vladlen Koltun: "Open3D: A modern library for 3D data processing", 2018 - http://www.open3d.org/
