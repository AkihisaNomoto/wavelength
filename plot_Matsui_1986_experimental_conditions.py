import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import configration as config

# Set global matplotlib parameters for font
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.get_cmap("Set1").colors)

# Constants
DATA_FILE_PATH = os.path.join(config.DATA_DIRECTORY, "Matsui_1986_spectral_irradiance_conditions.csv")

# Define radiation intensity (each condition is the same value)
radiation_intensity = 2000 # [W/m2]

# Read the data
df = pd.read_csv(DATA_FILE_PATH)
df.columns = ["wavelength", "Near- to mid-infrared (0.72–2.7 μm)", "Mid- to far-infrared radiation (1.5–4.8 μm)", "Far-infrared (6–20 μm)"]


# Convert wavelengths from nm to µm for plotting
x = df["wavelength"].values * 1e-3  # Convert to µm

# Calculate the spectral irradiance for each region and convert units appropriately
y_near_to_mid_infrared = df["Near- to mid-infrared (0.72–2.7 μm)"].values * radiation_intensity * 1e2
y_mid_to_far_infrared = df["Mid- to far-infrared radiation (1.5–4.8 μm)"].values * radiation_intensity * 1e2
y_far_infrared = df["Far-infrared (6–20 μm)"].values * radiation_intensity * 1e2

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
plt.plot(x, y_near_to_mid_infrared, label="Near- to mid-infrared (0.72–2.7 μm)")
plt.plot(x, y_mid_to_far_infrared, label="Near-infrared (0.80 – 1.35 µm)")
plt.plot(x, y_far_infrared, label="Mid-infrared (1.70 – 2.30 µm)")

# Fill the area under each curve
plt.fill_between(x, y_near_to_mid_infrared, alpha=0.5)
plt.fill_between(x, y_mid_to_far_infrared, alpha=0.5)
plt.fill_between(x, y_far_infrared , alpha=0.5)

# Annotate regions on the plot
region_labels = [("Ultraviolet", 0.20), ("Visible", 0.6), ("Near-IR", 1.1), ("Mid-IR", 1.9)]
for label, position in region_labels:
    plt.text(position, 4150, label, ha="center", color="black", fontsize=10)

# Set the limits for y and x axes
plt.ylim(0,1500)
# plt.xscale("log")
plt.xlim(0, 20)


# Set the ticks for the y-axis
plt.yticks(ticks=[0,500,1000,1500])
plt.xticks(ticks=[0,5,10,15,20])

# Label the axes
plt.xlabel("Wavelength [μm]")
plt.ylabel("Spectral irradiance [W/(m²μm)]")
# plt.ylabel("Spectral irradiance [W/(m$\mathregular{^2}$μm)]")
# Adjust the layout and legend
# plt.tight_layout(rect=[0, 0, 1, 0.9])
plt.legend(bbox_to_anchor=(0.5, 1.23), ncol=2, loc='upper center',frameon=False,fontsize=10)

# Save and show the figure
plt.savefig(os.path.join(config.FIGURE_DIRECTORY, "Matsui_1986_iradiation_conditions.svg"))
plt.show()




plt.figure(figsize=(6,3.5))
plt.plot(x, y1, label= "A (0.72 - 2.7 µm)")
plt.plot(x, y2, label= "B (1.5 - 4.8 µm)")
plt.plot(x, y3, label= "C (6 - 20 µm)")
plt.fill_between( x, y1, alpha=0.5)
plt.fill_between( x, y2, alpha=0.5)
plt.fill_between( x, y3, alpha=0.5)

plt.ylim(0,1500)
plt.xlim(0,20)
plt.yticks(ticks=[0,500,1000,1500])
plt.xticks(ticks=[0,5,10,15,20])
plt.xlabel("Wavelength [μm]")
plt.ylabel("Spectral irradiance [W/(m$\mathregular{^2}$μm)]")
plt.tight_layout(rect=[0,0,1,0.97])
plt.legend(bbox_to_anchor=(0.5, 1.18), ncol=3, loc='upper center',frameon=False,fontsize=10)

plt.savefig(FIGPATH + "B&E_MSM_Matsui1986_IradiationConditions.svg")
plt.show()