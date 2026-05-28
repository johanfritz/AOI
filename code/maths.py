import numpy as np
import scipy.sparse as sparse


def d_dlat(f, lat, lon=None):
    lat_rad = np.deg2rad(lat)
    R = 6.371e6
    latdim = len(lat)
    delta_lat = lat_rad[2] - lat_rad[1]
    delta_lat *= R
    d_lat = np.eye(latdim, latdim, 1) - np.eye(
        latdim, latdim, -1
    )  # central difference scheme
    d_lat[[0, 1], 0] = [-2, 2]  # + half-distance approximation for boundary
    d_lat[[-2, -1], -1] = [-2, 2]
    df_dlat = d_lat @ f / (2 * delta_lat)
    return df_dlat

def d_dlon(f, lat, lon):
    lon_rad = np.deg2rad(lon)
    lat_rad = np.deg2rad(lat)
    R = 6.371e6  # radius of Earth
    latdim = len(lat)
    londim = len(lon)
    delta_lon = lon_rad[2] - lon_rad[1]
    delta_lon *= R
    Delta_lon = delta_lon * np.cos(lat_rad)
    d_lon = np.eye(londim, londim, -1) - np.eye(londim, londim, 1)
    d_lon[0, -1] = -1
    d_lon[-1, 0] = 1
    df_dlon = f @ d_lon / (2 * Delta_lon.reshape(latdim, 1))
    return df_dlon

def absolute_vorticity(u,v, lat, lon):
    dv_dlon=d_dlon(v, lat, lon)
    du_dlat=d_dlat(u, lat, lon)
    latdim=len(lat)
    lat_rad=np.deg2rad(lat)
    R = 6.371e6
    zeta = dv_dlon - du_dlat + u * np.tan(lat_rad).reshape(latdim, 1) / R
    return zeta + 2 * 7.2821e-5 * np.sin(lat_rad).reshape(latdim, 1)

def stationary_wavenumber(q_y, u, lat, threshold=1.0):
    R = 6.371e6
    Ks2 = q_y/np.where(u<threshold, np.NaN, u)
    Ks = np.sqrt(np.where(Ks2<0, np.NaN, Ks2))   # sqrt, but only where Ks2 > 0 and u > threshold
    Ks[:2, :] = np.nan
    Ks[-2:, :] = np.nan
    return Ks * R

    


if __name__ == "__main__":
    from sampling import *

    u, v, lat, lon = load_data(resolution=1.25)
    Av = absolute_vorticity(u, v, lat, lon)
    dq_dy=d_dlat(Av, lat, lon)
    from plots import *
    #plot_contourf(np.clip(dq_dy, -1e-10, 2e-10), lat, lon, cbar=True, fixzero=True, vmin=-3e-10, vmax=6e-10)
    plot_contourf(np.clip(stationary_wavenumber(dq_dy, u, lat, threshold=1),0, 20), lat, lon, cbar=True, cmap="viridis")
