# dataset_D3D_100
Fancy version of the D3D-100 dataset

This repository includes the definition of the D3D-100 dataset as well as routines to instantiate
it so that it works with [D3D_loader](https://github.com/PlasmaControl/d3d_loaders).

To instantiate this dataset, ready to be used, run

```sh
$ instantiate.sh
```

This will fetch the data from D3D and calculate normalizations.
Make sure to run this script on a machine that has access to the D3D MDSplus server.
