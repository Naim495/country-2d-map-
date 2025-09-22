import rasterio
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# DEM file (GeoTIFF) - Example SRTM data
DEM_PATH = r"F:/python_code/map_app/data/dem_sample.tif"

# Open DEM
with rasterio.open(DEM_PATH) as dem:
    elevation = dem.read(1)  # elevation data
    bounds = dem.bounds
    transform = dem.transform

# Create coordinate grid
rows, cols = elevation.shape
x = np.arange(cols) * transform[0] + bounds.left
y = np.arange(rows) * transform[4] + bounds.top
X, Y = np.meshgrid(x, y)

# Mask no-data values
elevation = np.where(elevation < 0, np.nan, elevation)

# Plot 3D surface
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")

# Custom colormap: white→green for low, white→red for high
colors = np.empty(elevation.shape, dtype=object)
colors[:] = "white"
colors[elevation < 500] = "green"
colors[(elevation >= 500) & (elevation < 1500)] = "yellow"
colors[elevation >= 1500] = "red"

ax.plot_surface(X, Y, elevation, facecolors=colors,
                rstride=5, cstride=5, linewidth=0, antialiased=False)

ax.set_title("3D Elevation Map")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_zlabel("Elevation (m)")

plt.show()
