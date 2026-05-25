from sampling import load_data, downsample
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np


def plot_contourf(
    f, lon, lat, title=None, cbar=False, coast=True, savepath=None, *kwargs
):
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines() if coast else None
    plt.contourf(lon, lat, f)
    plt.colorbar() if cbar else None
    plt.title(title) if title is not None else None
    plt.savefig("figs/" + savepath) if savepath is not None else None
    plt.show()
