#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
import numpy as np
import logging
import multiprocessing as mp
import yaml
from os.path import join
import h5py





# Each task fetches a single variable from all shots and calculates the channel-wise
# mean and standard deviation.


def process_variable(args):
    """Fetch a single variable from all shots and calculate the channel-wise mean and std.

    args:
        datadir (string): Directory to HDF5 files
        group_name (string): HDF5 group name for the variable to calculate mean,std for
        shotlist (list[Int]): List of shots to process

    """
    datadir, group_name, shotlist = args
    # 1. Cache the relevant data from list of hdf5 files
    cache_data = []
    for shotnr in shotlist:
        with h5py.File(join(datadir, f"{shotnr}.h5"), "r") as df:
            cache_data.append(df[group_name]["zdata"][:])

    #for signal in cache_data:
    #    print(signal.shape)
    all_signals = np.hstack(cache_data)


    # 2. Calculate mean and std. Convert numpy datatypes to float. Otherwise yaml.safe_dump
    #    throws an error
    return {group_name: {"mean": float(all_signals.mean()), "std": float(all_signals.std())}}

    
def hello(args):
    ix, pred, shot_list = args
    print(f"Hello, ix={ix}, pred={pred}, shot_list={shot_list}")

if __name__ == "__main__":
    print("main")

    logging.basicConfig(filename="instantiate.log",
                    format="%(asctime)s    %(message)s",
                    encoding="utf-8",
                    level=logging.INFO)

    parser = argparse.ArgumentParser(
        prog="downloader.py",
        description="Downloads D3D datasets according to yaml description")
    parser.add_argument("--dataset_def", type=str,
        help="YAML file that contains definition of the dataset")
    parser.add_argument("--destination", type=str,
        help="Destination for Dataset HDF5 files")
    parser.add_argument("--signal_defs_0d", type=str,
        default="signals_0d.yaml",
        help="YAML file that contains 0d signal informations")
    parser.add_argument("--signal_defs_1d", type=str,
        default="signals_1d.yaml",
        help="YAML file that contains 1d signal informations")

    args = parser.parse_args()


    with open(args.dataset_def, "r") as stream:
        dataset_def = yaml.safe_load(stream)

    with open(args.signal_defs_0d, "r") as stream:
        signals_0d = yaml.safe_load(stream)

    # Generate list from shots in the dataset
    shot_list = list(dataset_def["shots"].keys())

    # The data is not stored by the alias of the predictor, but under the field `map_to` in signals?.yaml
    # Load the yaml files and find the map_to names that correspond to the field 'predictors' in the 
    # dataset definition yaml file
    group_list = [signals_0d[k]["map_to"] for k in dataset_def["predictors"]]


    pool = mp.Pool(12)
    res_mean_std = pool.map(process_variable,  [("D3D_100", grp, shot_list) for grp in group_list])

    # all_mean_std is a list of dicts: [{"var1": (mean, std)}, {"var2": (mean, std)}]
    # combine them into a single dict
    dict_mean_std = {}
    for i in res_mean_std:
        dict_mean_std.update(i)

    
    with open("normalization.yaml", "w") as fp:
        fp.write(yaml.safe_dump(dict_mean_std))
    





# end of file calculate_mean_std.py