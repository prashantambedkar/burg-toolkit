# BURG toolkit

This becomes a Python toolkit for **B**enchmarking and **U**nderstanding **R**obotic **G**rasping. Features are:
- visualize scenes generated with the sceneGeneration_MATLAB project
- visualize dense ground truth grasps from [Eppner et al., 2019](#references)
- algorithms for grasp sampling (future)
- evaluate grasp similarity as well as grasp coverage of sampler w.r.t. to the ground truth set

## project structure

The project contains the following directories:
- **docs** - configuration files to create documentation with sphinx
- **burg_toolkit** - the core Python library, used for io, mesh and point cloud processing, data visualization, etc.
- **scripts** - entry points, scripts for exploring the data, compiling datasets, evaluation
- **config** - configuration files, specifying e.g. important paths, which meshes to use, scale factors, etc.
- **data** - simple data samples which allow to use the scripts

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
This will also install all required dependencies. If you experience any problems, please open an issue.

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
- grasp sampler
    - implement option to use random rotation offset for creating grasp orientations
    - universal grasp representation: add required opening width and required grasping depth and filter grasps accordingly
- simulation-based grasp assessment using pybullet
    - determine simulation-based grasp success rate for grasp sets

### longer-term todos:
- task-oriented grasp sampling based on source/target scene
- io: move functionality related to a certain paper or approach to particular reader-class
- create new scenes with pybullet
- render new depth images for existing scenes
- once newer version of o3d comes with collision detection, try to get rid of trimesh dependency
- implement rule-based evaluation, e.g. for precision metrics from eppner2019
- implement analytic success metrics (force-closure) from fang2020, or ferrari-canny
- make repo public and use ReadTheDocs (once it is a bit more useful)

## References

- Clemens Eppner, Arsalan Mousavian and Dieter Fox: "A Billion Ways to Grasps - An Evaluation of Grasp Sampling Schemes on a Dense, Physics-based Grasp Data Set", ISRR 2019 - https://sites.google.com/view/abillionwaystograsp
- Qian-Yi Zhou, Jaesik Park, and Vladlen Koltun: "Open3D: A modern library for 3D data processing", 2018 - http://www.open3d.org/
