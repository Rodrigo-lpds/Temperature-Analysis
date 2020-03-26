#!/usr/bin/python3
# -*- coding: utf-8 -*-
#!/home/cendas/miniconda3/envs/DataEnv/bin/python3
#=========================# Required libraries ===========================================================
import sys # Import the "system specific parameters and functions" module
import matplotlib

import matplotlib.pyplot as plt # Import the Matplotlib package
from mpl_toolkits.basemap import Basemap # Import the Basemap toolkit&amp;amp;amp;amp;lt;/pre&amp;amp;amp;amp;gt;
import numpy as np # Import the Numpy package
from numpy.ma import masked_array
from remap import remap # Import the Remap function

from cpt_convert import loadCPT # Import the CPT convert function
from matplotlib.colors import LinearSegmentedColormap # Linear interpolation for color maps

import datetime # Library to convert julian day to dd-mm-yyyy
import time 

from matplotlib.patches import Rectangle # Library to draw rectangles on the plot
from osgeo import gdal # Add the GDAL library

matplotlib.use('Agg') # use a non-interactive backend
from netCDF4 import Dataset # Import the NetCDF Python interface
#======================================================================================================

# Load the Data =======================================================================================
# Path to the GOES-16 image file
path = sys.argv[1]

# Open the file using the NetCDF4 library
nc = Dataset(path)

# Get the latitude and longitude image bounds
geo_extent = nc.variables['geospatial_lat_lon_extent']
min_lon = float(geo_extent.geospatial_westbound_longitude)
max_lon = float(geo_extent.geospatial_eastbound_longitude)
min_lat = float(geo_extent.geospatial_southbound_latitude)
max_lat = float(geo_extent.geospatial_northbound_latitude)

# Choose the visualization extent (min lon, min lat, max lon, max lat)

# Rio de Janeiro as a Center of the projection
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

# Search for the GOES-16 channel in the file name
bandSetted = False

bands = ['M6C','M3C'] 
bandLenghts = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16']

mode = 0

while not bandSetted: 
    Band = (path[path.find(bands[mode])+3:path.find("_G16")])
    #if (len(Band) != 2) and (Band not in bandBounds):
    if (Band not in bandLenghts):    
        mode +=1  
    else:
        bandSetted = True    

# Read the data returned by the function 
if int(Band) <= 6:
    data = grid.ReadAsArray()
else:
    # If it is an IR channel subtract 273.15 to convert to ° Celsius
    data = grid.ReadAsArray() - 273.15
    # Make pixels outside the footprint invisible
    data[data <= -180] = np.nan
#=====================================================================================================

# Define the size of the saved picture=================================================================
DPI = 150
fig = plt.figure(figsize=(data.shape[1]/float(DPI), data.shape[0]/float(DPI)), frameon=False, dpi=DPI)

#print(data.shape)

ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
ax = plt.axis('off')
#======================================================================================================

# Plot the Data =======================================================================================

# Create the basemap reference for the Rectangular Projection
bmap = Basemap(llcrnrlon=extent[0], llcrnrlat=extent[1], urcrnrlon=extent[2], urcrnrlat=extent[3], epsg=4326)

# Draw the countries and Brazilian states shapefiles
bmap.readshapefile('/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Shapefiles/BRA_adm1','BRA_adm1',linewidth=0.10,color='#000000')
bmap.readshapefile('/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Shapefiles/ne_10m_coastline','ne_10m_0_coastline',linewidth=0.10,color='#000000')

# Draw parallels and meridians
bmap.drawparallels(np.arange(-90.0, 90.0, 5), linewidth=0.3, dashes=[4, 4], color='white', labels=[True,False,False,True], fmt='%g', labelstyle="+/-", size=10)
bmap.drawmeridians(np.arange(0.0, 360.0, 5), linewidth=0.3, dashes=[4, 4], color='white', labels=[True,False,False,True], fmt='%g', labelstyle="+/-", size=10)

dataA = masked_array(data,data<-20) #TIRA OS MENORES QUE -20
dataB = masked_array(data,data>=-20)#TIRA OS MAIORES QUE -20

if int(Band) <=7 or int(Band) == 15:
    # Converts a CPT file to be used in Python
    cpt = loadCPT('/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Colortables/Square Root Visible Enhancement.cpt')
    # Makes a linear interpolation
    cpt_convert = LinearSegmentedColormap('cpt', cpt)
    # Plot the GOES-16 channel with the converted CPT colors (you may alter the min and max to match your preference)
    bmap.imshow(data, origin='upper', cmap=cpt_convert, vmin=0, vmax=1)  

elif  int(Band) >7 and int(Band) <=10:
    # Converts a CPT file to be used in Python
    cptB = loadCPT('/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Colortables/GMT_hot.cpt')   
    cptA = loadCPT('/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Colortables/Square Root Visible Enhancement.cpt')
    # Makes a linear interpolation
    cpt_convertA = LinearSegmentedColormap('cpt', cptA) 
    cpt_convertB = LinearSegmentedColormap('cpt', cptB) 
    # Plot the GOES-16 channel with the converted CPT colors (you may alter the min and max to match your preference)
   
    pa = bmap.imshow(dataB, origin='upper', cmap=cpt_convertA, vmin=-80, vmax=-20)       
    pb = bmap.imshow(dataA, origin='upper', cmap=cpt_convertB, vmin=-20, vmax=-5) 


elif (int(Band) > 10 and int(Band) <= 14) or (int(Band) == 16):
   # Converts a CPT file to be used in Python
   cptB = loadCPT('/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Colortables/Rainbow.cpt')   
   cptA = loadCPT('/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Colortables/Square Root Visible Enhancement.cpt')
   # Makes a linear interpolation
   cpt_convertA = LinearSegmentedColormap('cpt', cptA) 
   cpt_convertB = LinearSegmentedColormap('cpt', cptB) 
   # Plot the GOES-16 channel with the converted CPT colors (you may alter the min and max to match your preference)
   
   pa = bmap.imshow(dataA, origin='upper', cmap=cpt_convertA, vmin=-20, vmax=100)       
   pb = bmap.imshow(dataB, origin='upper', cmap=cpt_convertB, vmin=-80, vmax=-20) 

if int(Band) <=7 or int(Band) == 15:
    # Insert the colorbar at the bottom
    cb = bmap.colorbar(location='right', size = '8.0%', pad = '4%', ticks=[20, 40, 60, 80])    
    cb.ax.set_xticklabels(['20', '40', '60', '80'])
else:
    # Insert the colorbar at the bottom
    cb = bmap.colorbar(location='right', size ='4.0%', pad = '8%')

cb.outline.set_visible(False)# Remove the colorbar outline
cb.ax.tick_params(width = 0)# Remove the colorbar ticks 
cb.ax.yaxis.set_tick_params(pad=-4)# Put the colobar labels inside the colorbar
#cb.ax.tick_params(axis='x', colors='yellow', labelsize=100)  # Change the color and size of the colorbar labels
#cb.ax.yaxis.set_tick_params(pad = -10) 
cb.ax.yaxis.set_ticks_position('right') 
cb.ax.tick_params(labelsize=10) 

# Search for the Scan start in the file name
Start = (path[path.find("_s")+2:path.find("_e")])


# Create a GOES-16 Bands string array
Wavelenghts = ['[]','[0.47 μm]','[0.64 μm]','[0.865 μm]','[1.378 μm]','[1.61 μm]','[2.25 μm]','[3.90 μm]','[6.19 μm]','[6.95 μm]','[7.34 μm]','[8.50 μm]','[9.61 μm]','[10.35 μm]','[11.20 μm]','[12.30 μm]','[13.30 μm]']

# Converting from julian day to dd-mm-yyyy
year = int(Start[0:4])
dayjulian = int(Start[4:7]) - 1 # Subtract 1 because the year starts at "0"
dayconventional = datetime.datetime(year,1,1) + datetime.timedelta(dayjulian) # Convert from julian to conventional
date = dayconventional.strftime('%d-%b-%Y') # Format the date according to the strftime directives
timeScan = Start [7:9] + ":" + Start [9:11] + ":" + Start [11:13] # Time of the Start of the Scan
Id = Start
# Get the unit based on the channel. If channels 1 trough 6 is Albedo. If channels 7 to 16 is BT.
if int(Band) <= 6:
    Unit = "Refletancia"
else:
    Unit = "Temperatura de Topo de Nuvem [°C]"
 
# Choose a title for the plot
Title = " GOES-16 ABI CMI Band " + str(Band) + "       " + Unit + "       " + date + "       " + timeScan + " UTC"
Latitude = "Latitude"
Longitude = "Longitude"
ColorBarLegend = "Temperatura de Topo de Nuvem [°C]"

# Add a black rectangle in the bottom to insert the image description
lon_difference = (extent[2] - extent[0]) # Max Lon - Min Lon
#currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((extent[0], extent[1]), lon_difference, lon_difference * 0.050, alpha=1, zorder=3, facecolor='black'))

# Add the image description inside the black rectangle
lat_difference = (extent[3] - extent[1]) # Max lat - Min lat
#plt.title(Title)
#plt.text(extent[0], extent[3] + lat_difference * 0.018,Title,horizontalalignment='left', color = 'black', size=10) 
#plt.text(extent[0], extent[3] + lat_difference * 0.018,Institution,horizontalalignment='left', color = 'black', size=10)
plt.text(extent[0] + lon_difference * 0.5, extent[3] + lat_difference * 0.035,Title, horizontalalignment='center', color = 'black', size=15)
plt.text(extent[0] + lon_difference * 0.5, extent[3] + lat_difference * 0.065," ", horizontalalignment='center', color = 'black', size=10)

plt.text(extent[0] + lon_difference * 0.5, extent[1] - lat_difference * 0.075,Longitude, horizontalalignment='center',color = 'black', size=15)
plt.text(extent[0] + lon_difference * 0.5, extent[1] - lat_difference * 0.15," ", horizontalalignment='center', color = 'black', size=18)    

plt.text(extent[0]- lon_difference * 0.15, extent[1] + lat_difference * 0.5 ,Latitude, verticalalignment ='center', rotation = "vertical", color = 'black', size=15) 
plt.text(extent[2] + lon_difference * 0.2, extent[1] + lat_difference * 0.5 ,ColorBarLegend, verticalalignment ='center', rotation = "vertical", color = 'black', size=15)

# Add logos / images to the plot
#logo_INPE = plt.imread('/home/cendas/Documents/VLAB/Logos/INPE Logo.png')
#logo_NOAA = plt.imread('/home/cendas/Documents/VLAB/Logos/NOAA Logo.png')
#logo_GOES = plt.imread('/home/cendas/Documents/VLAB/Logos/GOES Logo.png')
#plt.figimage(logo_INPE, 10, 40, zorder=3, alpha = 1, origin = 'upper')
#plt.figimage(logo_NOAA, 110, 40, zorder=3, alpha = 1, origin = 'upper')
#plt.figimage(logo_GOES, 195, 40, zorder=3, alpha = 1, origin = 'upper')

logo_Lamce = plt.imread("/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Logos/logo_lamce_RJ.png")
logo_Baia = plt.imread("/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Logos/baia_logo_RJ.png")


plt.figimage(logo_Lamce,  1300, 60, zorder=3, alpha = 1, origin = 'upper') 
plt.figimage(logo_Baia, 120, 60, zorder=3, alpha = 1, origin = 'upper')

seconds = time.time()
local_time = time.ctime(seconds)
time_saved = timeScan.replace(':','_')

dateData = local_time.split(" ")

try:
    date_saved = dateData[1] + '-' + dateData[3] + '-' + dateData[5]
except:
    date_saved = dateData[1] + '-' + dateData[2] + '-' + dateData[4]

# Save the result as a PNG
plt.savefig('/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Output/RJ/Projections/CH'+str(Band)+'/RJ_G16_C' + str(Band) + '_' + date + '_' + time_saved + 'UTC-ID_' + Id +'.tif', dpi=DPI, pad_inches=0, transparent=True)
plt.close()
 
# Add to the log file (called "G16_Log.txt") the NetCDF file name that I just processed.

# If the file doesn't exists, it will create one.
with open('/home/cendas/GOES16_WS_Rodrigo/CloudTopTemperature/Output/RJ/Projections/G16_Log.txt', 'a') as log:
 log.write(path.replace('\\\\', '\\') + '\n')
#======================================================================================================

# Export the result to GeoTIFF
#driver = gdal.GetDriverByName('GTiff')
#driver.CreateCopy('/home/cendas/GOES16-Files/Output/RJ/ProjectionsGEOTIF/CH'+str(Band)+'/RJ_G16_C' + str(Band) + '_' + date + '_' + time_saved+'.tif', grid, 0)
#======================================================================================================
