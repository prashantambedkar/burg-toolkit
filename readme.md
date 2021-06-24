# BURG toolkit

This is a Python toolkit for **B**enchmarking and **U**nderstanding **R**obotic **G**rasping, developed 
in the scope of [BURG project](#references) funded by CHIST-ERA / EPSRC. Features are:
- core data structures for object types and instances, scenes, grippers, grasps and grasp sets
- antipodal grasp sampling
- metrics for evaluation of grasps and grasp sets (analytic / simulation) [in progress]
- visualization of scenes and grasps
- interfaces to datasets, e.g.:
  - scenes generated with the sceneGeneration_MATLAB project
  - densely sampled ground truth grasps from [Eppner et al., 2019](#references)

## project structure

The project contains the following directories:
- **docs** - configuration files to create documentation with sphinx
- **burg_toolkit** - the core Python library, used for io, mesh and point cloud processing, data visualization, etc.
- **scripts** - entry points, scripts with examples, or for exploring the data, compiling datasets, evaluation
- **config** - configuration files, specifying e.g. important paths, which meshes to use, scale factors, etc.
- **data** - simple data samples which allow to use the examples

## first steps

### installation

The project requires Python 3.6-3.8 to work.
Older and newer versions are not supported.
Recommended way is to install in a virtual environment.
Go inside project main directory (where the `setup.py` resides) and execute:

```
# create virtual environment
python3 -m venv venv
source venv/bin/activate  # linux
.\venv\Scripts\Activate.ps1  # windows powershell

# might want to upgrade pip and packages required for setup
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel

# install burg_toolkit in editable mode
pip install -e .
```
This will also install all required dependencies*. 
Note that some steps may take a long time.
If you experience any problems, please open an issue or contact me.

You can check successful install by executing the script:
```
cd scripts
python grasp_testing.py
```

This should load a screwdriver object, sample some antipodal grasps and visualise them.
Note that there are some other scripts, but they require additional data to be downloaded.

*Note that python-fcl is only available for linux and will not be installed when using other platforms.
This package is used for mesh-mesh collision checks via trimesh and does not affect any other functionality.
Corresponding error messages should be easily recognisable.


### usage

Example:

```
import numpy as np
import burg_toolkit as burg

gs1 = burg.grasp.GraspSet.from_translations(np.random.random(50, 3))
gs2 = burg.grasp.GraspSet.from_translations(np.random.random(30, 3))
print('grasp coverage is:', burg.grasp.coverage(gs1, gs2))
```

See the scripts for more examples on usage and the docs for more detailed specifications.

### documentation

You should be able to build the documentation on the command line (with virtual environment activated) via:

```
sphinx-apidoc -f -o docs burg_toolkit
cd docs/
make html
```

The docs should then be in `docs/_build/html`folder.

## plans for the project
### todos
- render depth images for existing scenes/objects/instances
- grasp sampler
    - there is some unused code currently, needs better structure
    - more configurable AGS, e.g. with option to use random rotation offset for creating grasp orientations
    - more consistency in grasp representations, i.e. canonical forms, opening width, grasping depth etc.
- simulation-based grasp assessment using pybullet
    - determine simulation-based grasp success rate for grasp sets
- more reasonable constructors for grasp/graspset (hide internal arrays completely)
- refactor visualisation methods so that they are more concise and intuitive
- replace printouts and verbose flags with package-level logging
- update to open3d 0.13

### longer-term todos:
- task-oriented grasp sampling based on source/target scene
- io: move functionality related to a certain paper or approach to particular reader-class
- implement analytic success metrics (force-closure) from fang2020, or ferrari-canny
- use proper branching & merging and do some versioning
- make repo public and use ReadTheDocs (once it is a bit more useful).. PyPi?

## References

- BURG research project: https://burg.acin.tuwien.ac.at/
- Clemens Eppner, Arsalan Mousavian and Dieter Fox: "A Billion Ways to Grasps - An Evaluation of Grasp Sampling Schemes on a Dense, Physics-based Grasp Data Set", ISRR 2019 - https://sites.google.com/view/abillionwaystograsp
- Qian-Yi Zhou, Jaesik Park, and Vladlen Koltun: "Open3D: A modern library for 3D data processing", 2018 - http://www.open3d.org/
