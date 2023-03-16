#!/bin/bash

# Driver script to instantiate D3D-100 dataset


# 1. Instantiate dataset
python download.py --dataset_def d3d_100.yaml --destination D3D_100

# 2. Post-process:
# Generate time-to-disruption labels
python generate_ttd_targets.py --dataset_def d3d_100.yaml --destination D3D_100

# 3. Calculate mean and std averaged over signals
python calculate_mean_std.py --dataset_def d3d_100.yaml --destination D3D_100

# 4. Compile tmin from HDF5 files / dataset definition and write to yaml file
python compile_tmin.py --dataset_def d3d_100.yaml  --destination D3D_100

