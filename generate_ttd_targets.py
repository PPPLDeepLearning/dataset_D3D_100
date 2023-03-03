#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join
import yaml
import argparse
import logging
import numpy as np
import h5py

logging.basicConfig(filename="instantiate.log",
                    format="%(asctime)s    %(message)s",
                    encoding="utf-8",
                    level=logging.INFO)

parser = argparse.ArgumentParser(
    prog="generat_ttd_targets.py",
    description="Generate time-to-disruption target for each shot in the dataset")
parser.add_argument("--dataset_def", type=str,
    help="YAML file that contains definition of the dataset")
parser.add_argument("--destination", type=str,
    help="Destination for Dataset HDF5 files")

args = parser.parse_args()


with open(args.dataset_def, 'r') as fp:
    dataset_def = yaml.safe_load(fp)


for shotnr in dataset_def["shots"].keys():
    # Iterate over the target variables and find the longest time base
    # of the signals. Use this timebase to generate a ttd target
    with h5py.File(join(args.destination, f"{shotnr}.h5"), "a") as df:

        # Generate a time-to-disruption target, based on 1ms samples
        tb = np.arange(0.0, df.attrs["tmin"], 1.0)

        if dataset_def["shots"][shotnr]["ttd"] < 0.0:
            # Shot is disruptive, target is now a count-down
            target = tb.max() - tb
            taret = np.clip(target, 0.0, dataset_def["ttd_max"])
        else:
            # Shot is not disruptive. TTD is ttd_max (defined in yaml file)
            target = dataset_def["ttd_max"] * np.ones_like(tb)        
        target = np.log10(target + 0.1)

        logging.info(f"target_ttd = {target}")

        grp_t = df.create_group("target_ttd")
        grp_t.create_dataset("xdata", data=tb)
        grp_t.create_dataset("xdata": data=target)



    break



# end of file generate_ttd_targets.py