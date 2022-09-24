import pandas as pd
import geopandas as gpd
import numpy as np
import xarray as xr
import rioxarray
import rasterio as rio
from shapely.geometry import box, mapping
import matplotlib.pyplot as plt
import seaborn as sns
import rasterstats
import os
import glob

############################################################################################################
#SIMPLE RASTER SCRIPTS
############################################################################################################
#This will be a working document for basic raster functions using xarray, numpy, geopandas, etc.
#Please use the following code and edit as desired.


#2022-09-23: edited by Robin Kim
#HydroSense Lab - UVA ESE

########################################################################
#01 Open NETCDF File 

#Define file path
path = r'C:\...\DATA' 

#Define file type (e.i., .nc) 
# -- sorted will list in order numerically & alphabetically
# -- glob.glob will generate individual paths to all files
files = sorted(glob.glob(path+"/*.nc"))

# Open the desired dataset with xarray
dataset = xr.open_mfdataset(files[0],parallel=True,chunks={"lon": 100,"lat":200}) #-- parallelize with x/y coordinates if labels are known
#Sse smaller chunks if RAM is limited; larger chunks will render faster

# Experiment with indexing the dataset with []
# Check variables with dataset.variables

# See a plot by indexing the correct variable and executing the data with .plot()

#Extract lat/lon arrays for plotting 
ds_lat = dataset.y #or lat/latitude/etc. 
ds_lon = dataset.x #or lon/longitude/etc.
#Dimensions may also be renamed -- e.g., north_south to y || east_west to x
#ds.rename({'north_south': 'y', 'east_west': 'x'})


########################################################################
#02 Plot raster files 

#Define a function to plot numpy arrays
#Edit the figure size, colormap,title, etc. as needed
def plot_np(array,vmin,vmax,title):
    array = np.where(array==0,np.nan,array)
    fig1, ax1 = plt.subplots(figsize=(12,8))
    image = ax1.imshow(array,cmap = 'YlOrBr',vmin=vmin,vmax=vmax)
    cbar = fig1.colorbar(image,ax=ax1)
    ax1.set_title('{}'.format(title))
#Above function is useful for when you need to apply np calculations


######################################################################
#03 Clip NETCDF

#Define shapefile path and open with geopandas
shapename_path = r'C:\...\study_area.shp'
shapefile = gpd.read_file(shapename_path)  

#Make sure the dataset has a CRS, and then it may be clipped with the shapefile's properties
#Edit parameters as desired/needed.
clipped_file = dataset.rio.write_crs('epsg:4326').rio.clip(shapefile.geometry.apply(mapping), shapefile.crs, drop=True,all_touched=True)


######################################################################
#04 Save NETCDF as TIF

#Xarray to TIF
#Create a new data array with dimensions names, appropriate coordinate variable names and arrays, and variable name
new_array = xr.DataArray(dataset.variable[index], dims=("time","lat", "lon"), coords={"lat": ds_lat, "lon": ds_lon}, name="lst_celsius")
#Set appropriate coordinate reference system
new_array.rio.set_crs("epsg:4326")
#Set spatial dimensions for GeoTIF
new_array.rio.set_spatial_dims('lon','lat',inplace=True)
#Save to filepath
new_array.rio.to_raster(r'C:\...\__.tif')
