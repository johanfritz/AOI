import numpy as np

def load_data(resolution=2.5):
    assert resolution in [0.25, 0.5, 0.75, 1, 1.0, 1.25, 1.5, 2, 2.0, 2.25, 2.5]
    data = np.load("code/djf_mean.npz")
    (u, v, lat, lon)=(data["u"], data["v"], data["lat"], data["lon"])
    if resolution==0.25:
        return u, v, lat, lon
    n_lat=int(180/resolution)
    n_lon=int(360/resolution)
    u_coarse = np.zeros((n_lat, n_lon))
    v_coarse = np.zeros_like(u_coarse)
    u = u[1:, :]
    v = v[1:, :]
    space=int(resolution/0.25)
    for i in range(n_lat):
        for j in range(n_lon):
            u_coarse[i, j] = np.mean(u[space * i : space * (i + 1), space * j : space * (j + 1)])
            v_coarse[i, j] = np.mean(v[space * i : space * (i + 1), space * j : space * (j + 1)])
    lat = np.array([90 - resolution/2 - n * resolution for n in range(n_lat)])
    lon = np.array([resolution/2 + n * resolution for n in range(n_lon)])
    return u_coarse, v_coarse, lat, lon
