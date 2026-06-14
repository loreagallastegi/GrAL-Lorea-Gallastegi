import xarray as xr
import numpy as np
import pandas as pd

   
def datuak_zabaldu(bideagpt,bidea2d,bidea3d,bideaep):

    dsgpt=xr.open_dataset(bideagpt)
    ds2d=xr.open_dataset(bidea2d)
    ds3d=xr.open_dataset(bidea3d)
    dsep=xr.open_dataset(bideaep)
    ds=xr.merge([dsgpt, ds2d, ds3d,dsep],compat='no_conflicts', join='outer')  
    ds["z"]=ds["z"].sel(pressure_level=100)

    return ds

def ibilbidea_irakurri(fitxategia_excel):
    ibil=pd.read_excel(fitxategia_excel)  
    return ibil["lat"].values, ibil["lon"].values, ibil["time"].values
    

def kutxa_lortu(ds,t,lat_zen,lon_zen):
    ds_temp=ds.sel(valid_time=t, method="nearest") 
    
    lat_ind=np.abs(ds_temp["latitude"]-lat_zen).argmin().item()
    lon_ind=np.abs(ds_temp["longitude"]-lon_zen).argmin().item()
    
    kutxa = ds_temp.isel(latitude=slice(lat_ind-2,lat_ind+3),longitude=slice(lon_ind-2,lon_ind+3)) 
    return kutxa








