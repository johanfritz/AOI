import numpy as np
import xarray as xr
import time


def read_mean(filename="code/data_stream-moda_stepType-avgua.nc"):
    import time

    ds = xr.open_dataset(filename)
    u = np.zeros((721, 1440))
    v = np.zeros_like(u)
    djf_indices = np.where(ds.valid_time.dt.month.isin([12, 1, 2]).values)[0]
    print(len(djf_indices))
    for t1, t2, in zip([0, 50, 100, 150, 200, 250], [50, 100, 150, 200, 250, len(djf_indices)]):
        t0=time.time()
        u+=ds['u'].isel(valid_time=djf_indices[t1:t2]).squeeze().mean(dim="valid_time").values*(t2-t1)/len(djf_indices)
        v+=ds['v'].isel(valid_time=djf_indices[t1:t2]).squeeze().mean(dim="valid_time").values*(t2-t1)/len(djf_indices)
        print(f"Finished range {(t1, t2)} in {time.time()-t0} seconds")
    return u, v, ds.latitude.values, ds.longitude.values

u, v, lat, long=read_mean()
np.savez("djf_mean.npz", u=u, v=v, lat=lat, lon=long)
np.save("u.npy", u)
np.save("v.npy", v)
np.save("lat.npy", lat)
np.save("long.npy", long)