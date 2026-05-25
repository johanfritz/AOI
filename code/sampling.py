import numpy as np


def load_data():
    data = np.load("code/djf_mean.npz")
    return data["u"], data["v"], data["lat"], data["lon"]


def downsample(u, v, lat, lon):
    u_coarse = np.zeros((72, 144))
    v_coarse = np.zeros_like(u_coarse)
    u = u[1:, :]
    v = v[1:, :]
    for i in range(72):
        for j in range(144):
            u_coarse[i, j] = np.mean(u[10 * i : 10 * (i + 1), 10 * j : 10 * (j + 1)])
            v_coarse[i, j] = np.mean(v[10 * i : 10 * (i + 1), 10 * j : 10 * (j + 1)])
    lat = np.array([90 - 1.25 - n * 2.5 for n in range(72)])
    lon = np.array([1.25 + n * 2.5 for n in range(144)])
    return u_coarse, v_coarse, lat, lon


u, v, lat, lon = load_data()
u, v, lat, lon = downsample(u, v, lat, lon)