#!/usr/bin/python3
# -*- coding: utf-8 -*-
#!/home/cendas/miniconda3/envs/DataEnv/bin/python3

#=========================# Required libraries ===========================================================
# Import the NetCDF Python interface
from netCDF4 import Dataset 
# Import the Matplotlib package
import matplotlib 
import matplotlib.pyplot as plt # Collection of functions that make matplotlib work like MATLAB
from mpl_toolkits.basemap import Basemap # Import the Basemap toolkit
from matplotlib.colors import LinearSegmentedColormap # Linear interpolation for color maps
from matplotlib.patches import Rectangle # Library to draw rectangles on the plot
#Import the Numpy package
import numpy as np 
from numpy.ma import masked_array
# Add the GDAL library
from osgeo import gdal
# Import local functions
from remap import remap # Import the Remap function
from cpt_convert import loadCPT # Import the CPT convert function
from headerNetcdf import getBand,convertDate # Import band and convert date function
import sys
#======================================================================================================


# Load the Data =======================================================================================

# Path to the GOES-16 image file
#path = "..\\samples\\OR_ABI-L2-CMIPF-M6C13_G16_s20193010840381_e20193010850101_c20193010850198.nc"
path = "..\\samples\\OR_ABI-L2-CMIPF-M6C13_G16_s20193010800381_e20193010810100_c20193010810207.nc"
# Open the file using the NetCDF4 library

# Open the file using the NetCDF4 library
nc = Dataset(path)
#======================================================================================================

# Get the latitude and longitude image bounds
geo_extent = nc.variables['geospatial_lat_lon_extent']
min_lon = float(geo_extent.geospatial_westbound_longitude)
max_lon = float(geo_extent.geospatial_eastbound_longitude)
min_lat = float(geo_extent.geospatial_southbound_latitude)
max_lat = float(geo_extent.geospatial_northbound_latitude)

# Rio de Janeiro as a Center of the projection
# Choose the visualization extent (min lon, min lat, max lon, max lat)
extent = [-55, -35.0, -30.0, -10.0]

# Choose the image resolution (the higher the number the faster the processing is)
resolution = 2 

# Calculate the image extent required for the reprojection
H = nc.variables['goes_imager_projection'].perspective_point_height
x1 = nc.variables['x_image_bounds'][0] * H 
x2 = nc.variables['x_image_bounds'][1] * H 
y1 = nc.variables['y_image_bounds'][1] * H 
y2 = nc.variables['y_image_bounds'][0] * H 

# Call the reprojection funcion
grid = remap(path, extent, resolution,  x1, y1, x2, y2)

# Read the data returned by the function ==============================================================
# If it is an IR channel subtract 273.15 to convert to ° Celsius
data = grid.ReadAsArray() - 273.15
# Make pixels outside the footprint invisible
data[data <= -180] = np.nan
data = data[data<5]
#======================================================================================================
data_std = np.std(data)
data_mean = np.mean(data)
data_median = np.median(data)
print(data_std)
print(data_mean)
print(data_median)
#print(data.flatten().shape)
#plt.style.use('ggplot')
plt.hist(data.flatten(),bins=100)
plt.xlabel("Temperature °C")
plt.ylabel("Points")
#plt.plot(data.flatten(),normal)
#plt.savefig("C:\\Users\\Usuario\\Documents\\IC\\TemperatureCloudTop\\Temperature-Analysis\\src\\histogram.png")
plt.show()