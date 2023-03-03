#!/bin/bash

# Driver script to instantiate D3D-100 dataset

# 1. Update signal definitions (which define mapping from MDS/PTdata to HDF5)
# https://github.com/PlasmaControl/d3d_signals
echo "Pulling newest signal definitions"
cd d3d_signals && git pull
cd ..

# 2. Instantiate dataset
python download.py --dataset_def D3D_100.yaml --signal_defs_0d d3d_signals/signals_0d.yaml --signal_def_1d d3d_signals/signals_1d.yaml --destination D3D_100

# 3. Post-process:
# Generate time-to-disruption labels
python generate_ttd_targets.py

# Calculate mean and std averaged over signals
python calculate_mean_std.py
