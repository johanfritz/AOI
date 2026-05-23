import xarray as xr
import numpy as np

# Load the dataset
ds = xr.open_dataset('data_stream-moda_stepType-avgua.nc')  # Replace with your actual filename
print(ds.u)