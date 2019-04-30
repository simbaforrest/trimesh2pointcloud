#!/usr/bin/env bash
# mkdir /data/city/nyc/nyc_tri_pcds_4096
# python main.py -i /data/city/nyc/nyc_tri_objs -o /data/city/nyc/nyc_tri_pcds_4096 -n 4096
#python main.py -o /media/yuqiong/DATA/trimesh2pointcloud/test -i /media/yuqiong/DATA/trimesh2pointcloud/test -n 4096 -p 4
python main.py -o /media/yuqiong/DATA/city/nyc/nyc_tri_objs_sample -i /media/yuqiong/DATA/city/nyc/nyc_tri_pcds_4096_sample -n 4096 -p 4
