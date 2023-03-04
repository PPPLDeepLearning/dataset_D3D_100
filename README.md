# dataset_D3D_100
D3d_100 dataset for d3d_loaders

This repository includes the definition of the D3D-100 dataset as well as routines to instantiate
it so that it works with [D3D_loader](https://github.com/PlasmaControl/d3d_loaders).
Instantiating the dataset requires a copy of the [d3d_signals](https://github.com/PlasmaControl/d3d_signals) repository to translate predictor aliases to `MDS/PTDATA` point names. See the comments
in `instantiate.sh` to see where to clone it.

Run
```sh
$ instantiate.sh
```
to instantiate the dataset.

This will fetch the data from D3D and calculate normalizations.
Make sure to run this script on a machine that has access to the D3D MDSplus server.

Output of this script includes
* HDF5 data for the specified predictors in the subdirectory `D3D_100`.
* normalization coefficients (mean and standard deviation) in the file `normalization.yaml`






