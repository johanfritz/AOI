from sampling import load_data, downsample
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np


def plot_contourf(
    f, lat, lon, title=None, cbar=False, coast=True, savepath=None, fixzero=True, *kwargs
):
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines() if coast else None
    if fixzero and np.abs(lon[0])>1e-2:
        f=np.hstack([f, 0.5*(f[:, 0]+f[:, -1]).reshape(f.shape[0], 1)])
        lon=np.append(lon, [360]) 
        #sometimes does not work for some reason
    plt.contourf(lon, lat, f)
    plt.colorbar() if cbar else None
    plt.title(title) if title is not None else None
    plt.savefig("figs/" + savepath) if savepath is not None else None
    plt.show()


def plot_vectors(u, v, lat, lon, coast=True, mean=False):
    ax=plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines() if coast else None
    ax.quiver(lon, lat, u, v)
    plt.contourf(lon, lat, np.sqrt(u**2+v**2)) if mean else None
    plt.show()

if __name__ == "__main__":
    u, v,lat, lon=load_data()
    u, v, lat, lon=downsample(u, v, lat, lon)
    # print(u.shape)
    #plot_contourf(np.sqrt(u**2+v**2), lat, lon, cbar=True, fixzero=True)
    plot_vectors(u, v, lat, lon, mean=False)