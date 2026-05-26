import numpy as np
import scipy.sparse as sparse


def absolute_vorticity(u, v, lat, lon):
    lon_rad = np.deg2rad(lon)
    lat_rad = np.deg2rad(lat)
    R = 6.371e6  # radius of Earth
    latdim = len(lat)
    londim = len(lon)
    delta_lat=lat_rad[2]-lat_rad[1];delta_lat*=R
    delta_lon=lon_rad[2]-lon_rad[1];delta_lon*=R
    Delta_lon=delta_lon*np.cos(lat_rad)
    d_lat=np.eye(latdim, latdim, 1)-np.eye(latdim, latdim, -1) #central difference scheme
    d_lat[[0, 1], 0]=[-2, 2] #+ half-distance approximation for boundary
    d_lat[[-2, -1], -1]=[-2, 2]
    du_dlat=d_lat@u/(2*delta_lat)
    d_lon=np.eye(londim, londim, -1)-np.eye(londim, londim, 1)
    d_lon[0, -1]=-1
    d_lon[-1, 0]=1
    dv_dlon=v@d_lon/(2*Delta_lon.reshape(latdim, 1))
    zeta=dv_dlon-du_dlat+u*np.tan(lat_rad).reshape(latdim, 1)/R
    return zeta+2*7.2821e-5*np.sin(lat_rad).reshape(latdim, 1)


if __name__ == "__main__":
    from sampling import *

    u, v, lat, lon = load_data()
    u, v, lat, lon = downsample(u, v, lat, lon)
    Av=absolute_vorticity(u, v, lat, lon)
    from plots import *
    plot_contourf(Av, lat, lon, cbar=True, fixzero=True)
