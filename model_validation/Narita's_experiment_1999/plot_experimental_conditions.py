import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import configration as config

# Set global matplotlib parameters for font
plt.rcParams['font.family'] = 'Arial'

# Constants
DATA_FILE_PATH = "/data/Narita_1999_normalized_spectral_radiance.csv"

# Define radiation intensity (each condition is the same value)
radiation_intensity = 1220 # [W/m2]

# Read the data
df = pd.read_csv(DATA_FILE_PATH)
df.columns = ["wavelength", "Visible (0.30–0.84 µm)", "Near-infrared (0.80 – 1.35 µm)", "Mid-infrared (1.70 – 2.30 µm)"]


# Convert wavelengths from nm to µm for plotting
x = df["wavelength"].values * 1e-3  # Convert to µm

# Calculate the spectral irradiance for each region and convert units appropriately
y_visible = df["Visible (0.30–0.84 µm)"].values * radiation_intensity * 1e2
y_near_infrared = df["Near-infrared (0.80 – 1.35 µm)"].values * radiation_intensity * 1e2
y_mid_infrared = df["Mid-infrared (1.70 – 2.30 µm)"].values * radiation_intensity * 1e2

# Set up the plot
plt.figure(figsize=(6, 3.5))

# Define regions of interest with horizontal span and vertical lines
plt.axhspan(4000, 4500, color="lightgrey", alpha=0.3)
critical_lines = [0.4, 0.8, 1.4, 3.0]
for line in critical_lines:
    plt.axvline(line, 0, 4000, linestyle="dotted", color="lightgrey")

# Set ticks for the x-axis
plt.xticks([0, 0.4, 0.8, 1.4, 2.4])

# Plot each spectral irradiance region
plt.plot(x, y_visible, label="Visible (0.30 – 0.84 µm)")
plt.plot(x, y_near_infrared, label="Near-infrared (0.80 – 1.35 µm)")
plt.plot(x, y_mid_infrared, label="Mid-infrared (1.70 – 2.30 µm)")

# Fill the area under each curve
plt.fill_between(x, y_visible, alpha=0.5)
plt.fill_between(x, y_near_infrared, alpha=0.5)
plt.fill_between(x, y_mid_infrared, alpha=0.5)

# Annotate regions on the plot
region_labels = [("Ultraviolet", 0.20), ("Visible", 0.6), ("Near-IR", 1.1), ("Mid-IR", 1.9)]
for label, position in region_labels:
    plt.text(position, 4150, label, ha="center", color="black", fontsize=10)

# Set the limits for y and x axes
plt.ylim(0, 4500)
plt.xlim(0, 2.4)

# Set the ticks for the y-axis
plt.yticks(np.arange(0, 5000, 1000))

# Label the axes
plt.xlabel("Wavelength [μm]")
plt.ylabel("Spectral irradiance [W/(m²μm)]")

# Adjust the layout and legend
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.legend(bbox_to_anchor=(0.5, 1.23), ncol=2, loc='upper center',frameon=False,fontsize=10)

# Save and show the figure
plt.savefig(f"{config.FIGURE_PATH}Narita1999_IradiationConditions.svg")
plt.show()
