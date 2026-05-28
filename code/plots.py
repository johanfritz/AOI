from sampling import load_data
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import matplotlib.colors as mcolors


def plot_contourf(
    f, lat, lon, title=None, cbar=False, coast=True, savepath=None, fixzero=True, **kwargs
):
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines() if coast else None
    if fixzero and np.abs(lon[0])>1e-2:
        # f=np.hstack([f, 0.5*(f[:, 0]+f[:, -1]).reshape(f.shape[0], 1)])
        f=np.hstack([f,f[:, 0:1].reshape(f.shape[0], 1)])
        lon=np.append(lon, [360]) 
        #sometimes does not work for some reason
    cf = plt.contourf(lon, lat, f, **kwargs)
    plt.colorbar(cf) if cbar else None
    plt.title(title) if title is not None else None
    plt.savefig("figs/" + savepath) if savepath is not None else None
    plt.show()


def plot_vectors(u, v, lat, lon, coast=True, mean=False):
    ax=plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines() if coast else None
    ax.quiver(lon, lat, u, v)
    plt.contourf(lon, lat, np.sqrt(u**2+v**2)) if mean else None
    plt.show()