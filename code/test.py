import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

ds=xr.open_dataset("code/data_stream-moda_stepType-avgua.nc")
print(ds)
