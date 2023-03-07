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

        if dataset_def["shots"][shotnr]["ttd"] > 0.0:
            # Shot is disruptive, target is now a count-down
            tb = np.arange(0.0, dataset_def["shots"][shotnr]["ttd"], 1.0, dtype=np.float32)
            target = tb.max() - tb
            target = np.clip(target, 0.0, dataset_def["ttd_max"])
        else:
            # Shot is not disruptive. TTD is ttd_max (defined in yaml file)
            tb = np.arange(0.0, df.attrs["tmax"], 1.0)
            target = dataset_def["ttd_max"] * np.ones_like(tb)        

        target = np.log10(target + 0.1)

        logging.info(f"target_ttd = {target.shape}")

        try:
            if df["target_ttd"]["xdata"].size > 0:
                logging.info(f"TTD for shot {shotnr} already exists.")
                continue
        except KeyError:
            pass

        # This is only executed if the try/except block abvove passes
        # Write new ttd into hdf5 file
        grp_t = df.create_group("target_ttd")
        grp_t.create_dataset("xdata", data=tb.astype(np.float32))
        grp_t.create_dataset("zdata", data=target.astype(np.float32))



# end of file generate_ttd_targets.py
