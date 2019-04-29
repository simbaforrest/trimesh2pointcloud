'''
test.py in trimesh2pointcloud

author  : simbaforrest
created : 11/5/17 4:29 PM
'''

import os
import sys
import glob
from timeit import default_timer as timer
import argparse
import signal

import numpy as np

import pyximport; pyximport.install(inplace=True, reload_support=True)
from _trimesh2pointcloud import cy_trimesh2pointcloud as tri2pts
import multiprocessing
from timeit import default_timer as timer
from datetime import timedelta

def strip_slash(str1):
    slash_pos = str1.find('/')
    if slash_pos > -1:
        return int(str1[0:slash_pos])
    else:
        return int(str1)

def read_obj(fname):
    with open(fname) as f:
        content = f.readlines()

    content = [x.strip('\n') for x in content]
    content = [x.split() for x in content]

    type_col = np.array([row[0] for row in content])
    v_ind = np.where(type_col == 'v')[0]
    f_ind = np.where(type_col == 'f')[0]

    content = [x[1:4] for x in content]
    content = np.array(content)
    vertices = content[v_ind].tolist()
    faces = content[f_ind].tolist()

    vertices = np.array([[float(y) for y in x] for x in vertices])
    faces = np.array([[strip_slash(y) - 1 for y in x] for x in faces])
    return vertices, faces


def log_error(error_log, f):
    """
    log error to a file
    :param error_log: path to error log. ends with ".txt"
    :param f: obj file name
    :return:
    """
    with open(error_log, "a+") as e:
        e.write(f)
    return


def tri2pts_wrapper(V,G,num_points, return_dict):
    """
    a wrapper to pass the funciton tri2pts to the multiprocess manager
    :param V:
    :param G:
    :param num_points:
    :param return_dict:
    :return:
    """
    P = tri2pts(V,G,num_points)
    return_dict["res"] = P
    return


def main():
    # V=np.array([
    #     [1,0,0],
    #     [0,1,0],
    #     [0,0,1]
    # ], dtype=np.float32)
    # G=np.array([
    #     [0,1,2]
    # ], dtype=int)
    # k=1024
    # P = tri2pts(V,G,k)
    # print(P.shape)
    #
    # plt.figure()
    # ax=plt.subplot(111,projection='3d')
    # ax.plot(V[:,0],V[:,1],V[:,2],'b.')
    # ax.plot(P[:,0],P[:,1],P[:,2],'r.')
    # plt.sho
    p = argparse.ArgumentParser(description=
        """
        Use the command line argument parser in Python.
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.add_argument("-i", "--in_dir", required=True,
                   help="input directory of all .obj files ")
    p.add_argument("-o", "--out_dir", required=True,
                   help="output directory of all .npy files ")
    p.add_argument("-n", "--num_points", default=2048,
                   help="number of points per point cloud")
    args = p.parse_args()
    in_dir = args.in_dir
    out_dir = args.out_dir
    num_points = int(args.num_points)

    error_log = os.path.join(out_dir, "error.txt")
    try:
        os.remove(error_log)
    except OSError:
        pass

    ot_log = os.path.join(out_dir, "ot.txt")   # overtime log
    try:
        os.remove(ot_log)
    except OSError:
        pass

    # find all .obj files
    all_files = os.listdir(in_dir)
    all_obj = [x for x in all_files if x[-4:] == ".obj"]

    counter = 0
    start = timer()
    for i, f in enumerate(all_obj):
        if counter % 1000 == 0:
            end = timer()
            print(f)
            print("Processed: {0}-th file. Time elapsed: {1} s.".format(counter, timedelta(seconds=end-start)))
        counter += 1

        out_path = os.path.join(out_dir, f.split(".")[0] + ".npy")
        if os.path.exists(out_path):
            continue

        in_path = os.path.join(in_dir, f)
        V, G = read_obj(in_path)

        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p = multiprocessing.Process(target=tri2pts_wrapper, args=(V, G, num_points, return_dict))   # note the use of ,
        p.start()

        overtime = False   # check overtime error
        try:
            p.join(5)
        except Exception as e:
            print(e)
            log_error(error_log, f)
            continue
        if p.is_alive():
            overtime = True
            print("running overtime... let's kill it...")
            # Terminate
            p.terminate()
            p.join()

        if overtime:   # the process has been killed
            log_error(ot_log, f)
            continue
        else:
            result = return_dict["res"]   # resulting point cloud
            np.save(out_path, np.array(result))

    return
#    plt.figure()
#    ax=plt.subplot(111,projection='3d')
#    ax.plot(V[:,0],V[:,1],V[:,2],'b.')
#    ax.plot(P[:,0],P[:,1],P[:,2],'r.')
#    plt.show()

if __name__ == '__main__':
    main()
