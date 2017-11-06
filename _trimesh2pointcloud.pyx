'''
_trimesh2pointcloud.pyx

author  : cfeng
created : 11/05/17 11:45 AM
'''

# cimport openmp
cimport cython
# from cython.parallel cimport prange, parallel, threadid

from libcpp.vector cimport vector
import numpy as np
cimport numpy as np


cdef extern from "utils_sampling.hpp" namespace "Utils_sampling":
    void poisson_disk_raw(
        int nb_samples, const float *pVerts, const int nVerts,
        const int *pTris, const int nTris,
        vector[float] &sampled_pos
    )


@cython.boundscheck(False)
@cython.wraparound(False)
def _cy_trimesh2pointcloud(
    np.ndarray[np.float32_t, ndim=2, mode="c"]  V,
    np.ndarray[int, ndim=2, mode="c"]           G,
    int                                         k
    ):
    '''
    Input:
        V <Nx3>: tri-mesh vertices of N vertices
        G <Mx3>: tri-mesh indices of M triangles
        k <1>:   number of points to be sampled on the tri-mesh using poisson disk sampling
    Output:
        P <lx3>: sampled points, l almost equal to k
    '''
    cdef vector[float] Praw
    poisson_disk_raw(
        k,
        &V[0,0], V.shape[0],
        &G[0,0], G.shape[0],
        Praw
    )
    cdef np.ndarray P = np.array(Praw).reshape((Praw.size()/3, 3))
    return P


def cy_trimesh2pointcloud(V, G, k):
    V = np.require(V, dtype=np.float32, requirements=['C'])
    G = np.require(G, dtype=np.int32, requirements=['C'])
    k2= int(k)
    while True:
        P = _cy_trimesh2pointcloud(V, G, k2)
        if P.shape[0]<k:
            k2*=2
        else:
            break
    np.random.shuffle(P)
    return P[:k, :]