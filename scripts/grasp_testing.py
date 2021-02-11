import os
from timeit import default_timer as timer
import numpy as np
import configparser
import grasp_data_toolkit as gdt


def test_distance_and_coverage():
    # testing the distance function
    initial_translations = np.random.random((50, 3))
    gs = gdt.grasp.GraspSet.from_translations(initial_translations)

    theta = 0 / 180 * np.pi
    rot_mat = np.asarray([[1, 0, 0],
                          [0, np.cos(theta), -np.sin(theta)],
                          [0, np.sin(theta), np.cos(theta)]])

    grasp = gs[0]
    grasp.translation = np.asarray([0, 0, 0.003])
    grasp.rotation_matrix = rot_mat
    gs[0] = grasp

    theta = 15 / 180 * np.pi
    rot_mat = np.asarray([[np.cos(theta), 0, np.sin(theta)],
                          [0, 1, 0],
                          [-np.sin(theta), 0, np.cos(theta)]])

    grasp = gs[1]
    grasp.translation = np.asarray([0, 0, 0])
    grasp.rotation_matrix = rot_mat
    gs[1] = grasp

    dist = gdt.grasp.pairwise_distances(gs[0], gs[1])
    print('computation of pairwise_distances (15 degree and 3 mm)', dist.shape, dist)
    dist = gs[0].distance_to(gs[1])
    print('computation of distance_to (15 degree and 3 mm)', dist.shape, dist)

    t1 = timer()
    print('computation of coverage 20/50:', gdt.grasp.coverage_brute_force(gs, gs[0:20]))
    print('this took:', timer() - t1, 'seconds')

    t1 = timer()
    print('coverage kd-tree:', gdt.grasp.coverage(gs, gs[0:20], print_timings=True))
    print('this took:', timer() - t1, 'seconds')

    grasp_folder = 'e:/datasets/21_ycb_object_grasps/'
    grasp_file = '061_foam_brick/grasps.h5'
    grasp_set, com = gdt.io.read_grasp_file_eppner2019(os.path.join(grasp_folder, grasp_file))

    t1 = timer()
    # this is unable to allocate enough memory for len(gs)=500
    #print('computation of coverage 20/50:', gdt.grasp.coverage_brute_force(grasp_set, gs))
    #print('this took:', timer() - t1, 'seconds')

    t1 = timer()
    print('coverage kd-tree:', gdt.grasp.coverage(grasp_set, gs, print_timings=True))
    print('in total, this took:', timer() - t1, 'seconds')


def test_antipodal_grasp_sampling():
    # read config file
    cfg_fn = '../config/config.cfg'
    print('using config file in:', cfg_fn)

    cfg = configparser.ConfigParser()
    cfg.read(cfg_fn)

    # object lib
    print('read object library')
    object_library = gdt.io.read_object_library(cfg['General']['object_lib_fn'])
    print('found', len(object_library), 'objects')

    # find the foamBrick
    target_obj = []
    for obj in object_library:
        if obj.name == 'foamBrick':
            target_obj = obj
            print('using', target_obj.name, 'object')
            break

    # read the mesh as point cloud
    print('reading mesh and converting to point cloud')
    mesh_fn = os.path.join(
        cfg['General']['models_dir'],
        target_obj.name +
        cfg['General']['mesh_fn_ext']
    )
    point_cloud = gdt.mesh_processing.convert_mesh_to_point_cloud(mesh_fn, with_normals=True)

    # add them to object info
    target_obj.point_cloud = point_cloud
    target_obj.point_cloud[:, 0:3] -= target_obj.displacement

    grasp_set = gdt.sampling.sample_antipodal_grasps(
        target_obj.point_cloud,
        gdt.gripper.ParallelJawGripper(),
        n=10,
        visualize=False
    )
    print('grasp_set', grasp_set.internal_array.shape)

    # gdt.visualization.show_np_point_clouds(target_obj.point_cloud)


def test_rotation_to_align_vectors():
    vec_a = np.array([1, 0, 0])
    vec_b = np.array([0, 1, 0])
    r = gdt.util.rotation_to_align_vectors(vec_a, vec_b)
    print('vec_a', vec_a)
    print('vec_b', vec_b)
    print('R*vec_a', np.dot(r, vec_a.reshape(3, 1)))

    vec_a = np.array([1, 0, 0])
    vec_b = np.array([-1, 0, 0])
    r = gdt.util.rotation_to_align_vectors(vec_a, vec_b)
    print('vec_a', vec_a)
    print('vec_b', vec_b)
    print('R*vec_a', np.dot(r, vec_a.reshape(3, 1)))


if __name__ == "__main__":
    # test_distance_and_coverage()
    test_antipodal_grasp_sampling()
    # test_rotation_to_align_vectors()
