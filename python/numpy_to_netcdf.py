import os
import glob
import pandas as pd
import numpy as np
import geopandas as gpd
from datetime import date,datetime,timedelta
import rasterstats as rs
import xarray as xr
import rasterio as rio
import rioxarray
import matplotlib.pyplot as plt
from shapely.geometry import box, mapping
from rasterio.enums import Resampling
import gc


##################
#Numpy files to netcdf
modis_lst_shape = xr.open_rasterio(glob.glob('D:\processed-data\MODIS_LST\*.tif')[0]) #band,lat,lon -- y,x for modis
lat = np.array(modis_lst_shape.y)
lon = np.array(modis_lst_shape.x)

#Means
years = range(2003,2023)
for year in years:
    daily_dataframe = sorted(glob.glob(r'D:\processed-data\MODIS_LST\MOD11MYD21\DAILY\{}\*mean.npy'.format(year)))
    annual_doys = [int(file[-12:-9]) for file in daily_dataframe]
    annual_datetimes = [datetime(year, 1, 1) + timedelta(doy) for doy in annual_doys]
    annual_lst = [np.load(file) for file in daily_dataframe]

    dataarrays = [xr.DataArray(array,dims=('lat','lon'),coords={'lat':lat,'lon':lon},name='LST_K').rio.set_spatial_dims('lon','lat',inplace=True).rio.set_crs("epsg:4326")
                   for array in annual_lst]
    dataset = xr.concat(dataarrays,dim='time')
    dataset['time'] = annual_datetimes
    dataset.to_netcdf(r'D:\processed-data\MODIS_LST\MOD11MYD21\DAILY\{}\{}_mean.nc'.format(year,year))
    del annual_lst,dataarrays,dataset,annual_datetimes
    gc.collect()

#Errors
years = range(2003,2023)
for year in years:
    daily_dataframe = sorted(glob.glob(r'D:\processed-data\MODIS_LST\MOD11MYD21\DAILY\{}\*error.npy'.format(year)))
    annual_doys = [int(file[-13:-10]) for file in daily_dataframe]
    annual_datetimes = [datetime(year, 1, 1) + timedelta(doy) for doy in annual_doys]
    annual_lst = [np.load(file) for file in daily_dataframe]

    dataarrays = [xr.DataArray(array,dims=('lat','lon'),coords={'lat':lat,'lon':lon},name='LST_K').rio.set_spatial_dims('lon','lat',inplace=True).rio.set_crs("epsg:4326")
                   for array in annual_lst]
    dataset = xr.concat(dataarrays,dim='time')
    dataset['time'] = annual_datetimes
    dataset.to_netcdf(r'D:\processed-data\MODIS_LST\MOD11MYD21\DAILY\{}\{}_error.nc'.format(year,year))
    del annual_lst,dataarrays,dataset,annual_datetimes
    gc.collect()

