"""
This script translates the ShapeNetSem models used in ACRONYM into an ObjectLibrary, so it can be used within
the BURG toolkit.
"""

import argparse
import os
import pathlib
from functools import partial

import h5py
import numpy as np
import burg_toolkit as burg
import trimesh
import concurrent.futures


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--acronym_dir', type=str, default='/home/rudorfem/datasets/acronym/')
    parser.add_argument('--max_workers', type=int, default=24)
    return parser.parse_args()


def create_object_type(grasp_filename, acronym_dir):
    # Each shape must be translated into a burg.ObjectType. All ObjectTypes within one ObjectLibrary must have a
    # unique identifier, which is a bit troublesome as there are several duplicate shapes which only distinguish
    # themselves in the scale factor. They must be different ObjectTypes.

    cat, shape, _ = grasp_filename[:-len('.h5')].split('_')
    grasps = h5py.File(os.path.join(acronym_dir, 'grasps', grasp_filename), 'r')
    relative_mesh_fn = grasps['object/file'][()].decode('utf-8')
    original_mesh_fn = os.path.join(acronym_dir, relative_mesh_fn)
    centered_mesh_fn = os.path.join(acronym_dir, 'meshes_centered',
                                    pathlib.Path(*pathlib.Path(relative_mesh_fn).parts[1:]))
    burg.io.make_sure_directory_exists(os.path.join(acronym_dir, 'meshes_centered'))
    scale = float(grasps['object/scale'][()])  # rather read scale directly than from grasp filename

    # create object type: identifier=category_shape_scale
    # set all parameters
    obj = burg.ObjectType(
        identifier=f'{cat}_{shape}_{scale}',
        mesh_fn=centered_mesh_fn,
        mass=float(grasps['object/mass'][()]),
        friction_coeff=float(grasps['object/friction'][()]),
        scale=scale
    )

    # we also need to subtract the mean from the meshes and the center of mass
    mesh = trimesh.load(original_mesh_fn, file_type='obj')
    if isinstance(mesh, list):
        # do concatenation, this is fixed in a newer trimesh version:
        # https://github.com/mikedh/trimesh/issues/69
        mesh = trimesh.util.concatenate(mesh)
    tmesh_mean = np.mean(mesh.vertices, 0)
    mesh.vertices -= np.expand_dims(tmesh_mean, 0)
    mesh.visual = trimesh.visual.ColorVisuals()  # to prevent creation of a mtl file
    mesh.export(centered_mesh_fn)

    # create vhacd
    # duplicate shapes with different scales will have same VHACD file, as it is scaled during loading
    vhacd_dir = os.path.join(acronym_dir, 'vhacd', cat)
    burg.io.make_sure_directory_exists(vhacd_dir)
    vhacd_fn = os.path.join(vhacd_dir, f'{shape}.obj')
    if not os.path.isfile(vhacd_fn):
        obj.generate_vhacd(vhacd_fn)
    obj.vhacd_fn = vhacd_fn  # make sure object type has this property even if it did not generate vhacd itself

    # however, each object type has its own urdf file, as it is scale-specific
    # some parameters (inertia/com) are given in ACRONYM annotations, so let's use those directly
    urdf_dir = os.path.join(acronym_dir, 'urdf', cat)
    burg.io.make_sure_directory_exists(urdf_dir)
    urdf_fn = os.path.join(urdf_dir, f'{shape}_{scale}.urdf')
    rel_mesh_fn = os.path.relpath(vhacd_fn, os.path.dirname(urdf_fn))
    com = np.array(grasps['object/com'])
    com -= tmesh_mean * scale   # apply same offset as for mesh and vhacd, but need to consider scale factor here

    burg.io.save_urdf(urdf_fn, mesh_fn=rel_mesh_fn, name=obj.identifier, origin=[0, 0, 0],
                      inertia=np.array(grasps['object/inertia']), com=com,
                      mass=obj.mass, friction=obj.friction_coeff, scale=obj.scale,
                      overwrite_existing=True)
    obj.urdf_fn = urdf_fn
    print(f'completed {obj.identifier}')
    return obj


def main(args):
    acronym_dir = args.acronym_dir
    max_workers = args.max_workers

    lib = burg.ObjectLibrary(name='ACRONYM objects',
                             description='objects from ShapeNetSem, used for ACRONYM')
    lib.to_yaml(os.path.join(acronym_dir, 'object_library.yml'))

    grasp_annotation_dir = os.path.join(acronym_dir, 'grasps')

    # let's do some magic to the filenames to avoid same shapes being processed in parallel (as this would lead to a
    # concurrent.futures.process.BrokenProcessPool error).
    # note that there are not more than two ObjectTypes that share the same mesh
    # we sort the list, make a list of odd indices and one of even indices and concatenate them
    # this places the neighboring onces as far apart as possible
    sorted_filenames = sorted(os.listdir(grasp_annotation_dir))
    filenames = sorted_filenames[0::2] + sorted_filenames[1::2]

    # some shapes do not work.. let's keep track which ones and remove them right from the start
    ignore_shapes = [
        'TV_907b90beaf5e8edfbaf98569d8276423',              # vhacd segfaults, shape has weird dimensions
        'Bowl_fca9fcb710592311d291861d5bc3e7c8',            # not processed by manifold/simplify
        'PottedPlant_f01872cde4d81403504721639e19f609',     # not processed by manifold/simplify
        'PottedPlant_a7a42a3c8bb28103604096c107e7cc16',     # not processed by manifold/simplify
        'PottedPlant_dc6922b9eece4ab7e3f7a74e12a274ef',     # not processed by manifold/simplify
        'Washer_8ef93a18aca9f3bc69569e953575ec69',          # not processed by manifold/simplify
        'Ship_36fba9c2f4c256dc4387c5ea62cbbe8b',            # not processed by manifold/simplify
    ]
    for ignore_shape in ignore_shapes:
        filenames = [file for file in filenames if not file.startswith(ignore_shape)]

    multi_process = True
    if multi_process:
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            # execute concurrently, will take a while...
            object_types = executor.map(partial(create_object_type, acronym_dir=acronym_dir), filenames, chunksize=10)
    else:
        object_types = []
        for filename in filenames:
            object_types.append(create_object_type(filename, acronym_dir=acronym_dir))

    for obj in object_types:
        lib[obj.identifier] = obj
    lib.to_yaml()


if __name__ == '__main__':
    main(parse_args())