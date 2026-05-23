import rasterio
import numpy as np
import matplotlib.pyplot as plt

# DEM file path
dem_file = r"C:\Users\91827\Downloads\Charles_uni\River_profile_data\DEM_data.tif"

# Open DEM
with rasterio.open(dem_file) as src:
    dem = src.read(1)

# Remove no-data values
dem = np.where(dem < -1000, np.nan, dem)

# pixel resolution (SRTM is ~30m)
res = 30 
# Calculate gradient and divide by resolution
dx, dy = np.gradient(dem)
dx = dx / res
dy = dy / res
# Calculate slope in radians then convert to degrees
slope = np.sqrt(dx**2 + dy**2)
slope_deg = np.degrees(np.arctan(slope))

# Flatten arrays
elevation = dem.flatten()
slope_values = slope_deg.flatten()

# Remove NaN values
mask = ~np.isnan(elevation) & ~np.isnan(slope_values)

elevation = elevation[mask]
slope_values = slope_values[mask]

# Increase sample size for better analysis
sample_size = 20000

indices = np.random.choice(len(elevation), sample_size, replace=False)

elevation_sample = elevation[indices]
slope_sample = slope_values[indices]

# Create plot
plt.figure(figsize=(8,6))

scatter = plt.scatter(
    elevation_sample,
    slope_sample,
    c=elevation_sample,
    cmap="terrain",
    s=5,
    alpha=0.3
)

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label("Elevation (m)", fontsize=12.5)
cbar.ax.tick_params(labelsize=12.5)

# Labels and title
plt.xlabel("Elevation (m)", fontsize=12.5)
plt.ylabel("Slope (degrees)", fontsize=12.5)
plt.title("Slope vs Elevation Relationship", fontsize=12.5)

plt.xticks(fontsize=12.5)
plt.yticks(fontsize=12.5)

plt.grid(True)

plt.tight_layout()

plt.show()