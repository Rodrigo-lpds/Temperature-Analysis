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
#======================================================================================================


# Load the Data =======================================================================================

# Path to the GOES-16 image file
path = "..\\samples\\OR_ABI-L2-CMIPF-M6C13_G16_s20193010840381_e20193010850101_c20193010850198.nc"
# Open the file using the NetCDF4 library
nc = Dataset(path)
#======================================================================================================

# Get the latitude and longitude image bounds
geo_extent = nc.variables['geospatial_lat_lon_extent']
min_lon = float(geo_extent.geospatial_westbound_longitude)
max_lon = float(geo_extent.geospatial_eastbound_longitude)
min_lat = float(geo_extent.geospatial_southbound_latitude)
max_lat = float(geo_extent.geospatial_northbound_latitude)

# Bocaina as a Center of the projection
degrees = 0
# Choose the visualization extent (min lon, min lat, max lon, max lat)
#extent = [-47 - degrees ,-25 - degrees,-42+ degrees,-20 + degrees] #Bocaina
extent = [-44 - degrees ,-27 - degrees,-38+ degrees,-21 + degrees] #Regiao Norte Fluminense
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
#======================================================================================================
grid.GetRasterBand(1).WriteArray(data) # converte o grid para celsius
# Define the size of the saved picture =================================================================
DPI = 150
fig = plt.figure(figsize=(data.shape[1]/float(DPI), data.shape[0]/float(DPI)), frameon=False, dpi=DPI)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
ax = plt.axis('off')
#======================================================================================================

# Plot the Data =======================================================================================

# Create the basemap reference for the Rectangular Projection
bmap = Basemap(llcrnrlon=extent[0], llcrnrlat=extent[1], urcrnrlon=extent[2], urcrnrlat=extent[3], epsg=4326)

# Draw the countries and Brazilian states shapefiles
bmap.readshapefile('..\\shapefile\\BRA_adm1','BRA_adm1',linewidth=0.10,color='#000000')

# Draw parallels and meridians
#bmap.drawparallels(np.arange(-90.0, 90.0, 5), linewidth=0.3, dashes=[4, 4], color='white', labels=[True,False,False,True], fmt='%g', labelstyle="+/-", size=10)
#bmap.drawmeridians(np.arange(0.0, 360.0, 5), linewidth=0.3, dashes=[4, 4], color='white', labels=[True,False,False,True], fmt='%g', labelstyle="+/-", size=10)

#Split the dataset with temperatures above and below -20°C 
temp = -20
tempAbove= masked_array(data,data<temp)
tempBelow = masked_array(data,data>=temp)

# Converts a CPT file to be used in Python
cptRainbow = loadCPT('..\\colortable\\Rainbow.cpt')   
cptSquareRoot = loadCPT('..\\colortable\\Square Root Visible Enhancement.cpt')

# Makes a linear interpolation
cpt_convert_SquareRoot = LinearSegmentedColormap('cpt', cptSquareRoot) 
cpt_convert_Rainbow = LinearSegmentedColormap('cpt', cptRainbow) 

# Plot the GOES-16 channel with the converted CPT colors (you may alter the min and max to match your preference)
plot_SquareRoot = bmap.imshow(tempAbove, origin='upper', cmap=cpt_convert_SquareRoot, vmin=-20, vmax=100)       
plot_Rainbow = bmap.imshow(tempBelow, origin='upper', cmap=cpt_convert_Rainbow, vmin=-80, vmax=-20) 

# Insert the colorbar at the bottom
#cb = bmap.colorbar(location='right', size ='4.0%', pad = '8%')
#cb.outline.set_visible(False)   #   Remove the colorbar outline
#cb.ax.tick_params(width = 0)    #   Remove the colorbar ticks 
#cb.ax.yaxis.set_tick_params(pad=-4) # Put the colobar labels inside the colorbar
#cb.ax.yaxis.set_ticks_position('right') 
#cb.ax.tick_params(labelsize=10) 

# Converting from julian day to dd-mm-yyyy
new_date =  convertDate(path)
date,timeScan = new_date['date_strf'],new_date['time_Scan']

# Get the unit based on the channel. If channels 1 trough 6 is Albedo. If channels 7 to 16 is BT.
Unit = "Cloud Top Temperature [°C]"

# Choose a title for the plot
Band = getBand(path)
Title = " GOES-16 ABI CMI Band " + str(Band) + "       " + Unit + "       " + date + "       " + timeScan + " UTC"
Latitude = "Latitude"
Longitude = "Longitude"
ColorBarLabel = "Cloud Top Temperature [°C]"

# Add a black rectangle in the bottom to insert the image description
lon_difference = (extent[2] - extent[0]) # Max Lon - Min Lon
# Add the image description inside the black rectangle
lat_difference = (extent[3] - extent[1]) # Max lat - Min lat

#Labels and its positions
#plt.text(extent[0] + lon_difference * 0.5, extent[3] + lat_difference * 0.035,Title, horizontalalignment='center', color = 'black', size=15)
#plt.text(extent[0] + lon_difference * 0.5, extent[3] + lat_difference * 0.065," ", horizontalalignment='center', color = 'black', size=10)
#plt.text(extent[0] + lon_difference * 0.5, extent[1] - lat_difference * 0.075,Longitude, horizontalalignment='center',color = 'black', size=15)
#plt.text(extent[0] + lon_difference * 0.5, extent[1] - lat_difference * 0.15," ", horizontalalignment='center', color = 'black', size=18)    
#plt.text(extent[0] - lon_difference * 0.15, extent[1] + lat_difference * 0.5 ,Latitude, verticalalignment ='center', rotation = "vertical", color = 'black', size=15) 
#plt.text(extent[2] + lon_difference * 0.2, extent[1] + lat_difference * 0.5 ,ColorBarLabel, verticalalignment ='center', rotation = "vertical", color = 'black', size=15)

# Export the result to GeoTIFF
driver = gdal.GetDriverByName('GTiff')
driver.CreateCopy('Channel_13.tif', grid, 0)
