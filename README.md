# trimesh2pointcloud
cython wrapper of poisson disk sampling of a triangle mesh in vcglib

This program will output point cloud files

# Usage
`python main.py -i IN_DIR -o OUT_DIR -n NUM_POINTS`

where
- `IN_DIR` is the directory containing all `.obj` files
- `OUT_DIR` is the directory containing all output `.npy` files saving a point cloud  
- `NUM_POINTS` is the number of points per point cloud file
