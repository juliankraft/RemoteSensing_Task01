# Remote Sensing Assignment Task1

ZURICH UNIVERSITY OF APPLIED SCIENCES <br>
DEPARTMENT LIFE SCIENCES AND FACILITY MANAGEMENT <br>
Institute of Natural Resource Sciences

Task1 Modul Remote Sensing FS24

by: <br>
Julian Kraft

Bachelor's Program 2022  
Environmental Engineering  
Submission Date: 2024-04-08

## Description
This repository shares all the code related to this assignment.

## Data
The RawData files exceed the maximum file size for GitHub. They can be downloaded using the download_data.py file. A stable internet connection and a user account on the Copernicus platform are needed - it can be created free of charge on [copernicus.eu](https://openeo.dataspace.copernicus.eu/).

## Python Environment
The python environment used to download and process the data was created with anaconda using the following command:
```bash
conda create -n geodata_env -c conda-forge python=3 netcdf4 xarray matplotlib numpy dask rasterio rioxarray geopandas pandas cartopy tqdm openeo jupyterlab 
```

## Data Visualisation
The data visualization is done in the Jupyter Notebook file visualization.ipynb.