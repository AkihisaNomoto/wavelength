import os
import pandas as pd
import matplotlib.pyplot as plt
import configration as config

# Constants
DATA_FILE_PATH = "C:\\Users\\monyo\\PycharmProjects\\wavelength\\model_validation\\Nomoto's experiment_2021\\data\\filter_and_radiation_spectrum.xlsx"
FIGURE_SAVE_PATH = config.FIGURE_PATH  # You need to specify the actual save directory

# Read data from Excel file
df = pd.read_excel(DATA_FILE_PATH, sheet_name="Spectral properties")
df.columns = ["wavelength", "Filter A", "Filter B", "Radiation A", "Radiation B", "Radiation C"]

# Initialize subplot grid
fig, axes = plt.subplots(2, 1, sharex=True, figsize=(6, 6))

# Convert wavelength to micrometers and radiation to appropriate units
x = df["wavelength"].values * 1e-3  # Convert nanometers to micrometers
radiation_a = df["Radiation A"].values
radiation_b = df["Radiation B"].values
radiation_c = df["Radiation C"].values
filter_a_transmittance = df["Filter A"].values * 1e-2  # Convert percentage to fraction
filter_b_transmittance = df["Filter B"].values * 1e-2  # Convert percentage to fraction

# Define normalized radiation A
df['normalized_radiation_A'] = df['Filter A'] * df['Radiation A']
total = df['normalized_radiation_A'].sum()
df['normalized_radiation_A'] /= total
# Define normalized radiation B
df['normalized_radiation_B'] = df['Filter B'] * df['Radiation B']
total = df['normalized_radiation_B'].sum()
df['normalized_radiation_B'] /= total
# Define normalized radiation C (Radiation C is used as it is because there is no filter effect)
df['normalized_radiation_C'] = radiation_c
total = df['normalized_radiation_C'].sum()
df['normalized_radiation_C'] /= total

# Save the file as input summary
df.to_csv('input_summary.csv', index=False)

# Plot radiation levels
axes[0].plot(x, radiation_a, label="Radiation A")
axes[0].plot(x, radiation_b, label="Radiation B")
axes[0].plot(x, radiation_c, label="Radiation C")

# Plot filter transmittance
axes[1].plot(x, filter_a_transmittance, label="Filter A")
axes[1].plot(x, filter_b_transmittance, label="Filter B")

# Fill the areas under the radiation curves
axes[0].fill_between(x, radiation_a, alpha=0.5)
axes[0].fill_between(x, radiation_b, alpha=0.5)
axes[0].fill_between(x, radiation_c, alpha=0.5)

# Add vertical dotted lines at specified wavelengths
wavelength_markers = [0.4, 0.8, 1.4, 3.0]
for ax in axes:
    for wm in wavelength_markers:
        ax.axvline(wm, linestyle="dotted", color="lightgray")

# Set legends and axis properties
axes[0].legend(loc='upper left', bbox_to_anchor=(0, 0.93))
axes[1].legend(loc='upper left', bbox_to_anchor=(0, 1))

# Axis labels and scales
axes[0].set_ylabel("Relative spectral irradiance [-]")
axes[1].set_ylabel("Transmittance [-]")
axes[1].set_xlabel("Wavelength [μm]")

# Set x-axis to logarithmic scale
for ax in axes:
    ax.set_xscale("log")
    ax.set_xlim((0.1, 50))
    ax.tick_params(pad=6)

# Set y-axis limits
axes[0].set_ylim((0, 1.1))
axes[1].set_ylim((0, 1))

# Annotate spectral regions on the plot
spectral_regions = {
    "Ultraviolet": 0.21,
    "Visible": 0.56,
    "Near-IR": 1.05,
    "Mid-IR": 2.05,
    "Far-IR": 12.0
}
for region, position in spectral_regions.items():
    axes[0].text(position, 1.025, region, ha="center", fontsize=10)
axes[0].axhspan(1.0, 1.1, color="lightgray", alpha=0.3)  # Highlight spectral region labels background

# Tick parameters
for ax in axes:
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', length=2.5)

# Tight layout for better spacing
fig.tight_layout()
fig.align_labels()

# Add subplot labels ('a)' and 'b)')
subplot_labels = ['(a)', '(b)']
for i, ax in enumerate(axes):
    ax.text(-0.07, 1.0, subplot_labels[i], transform=ax.transAxes, fontsize=12, fontweight='bold', va='center', ha='right')

# Save the figure
if not os.path.exists(FIGURE_SAVE_PATH):
    os.makedirs(FIGURE_SAVE_PATH)
fig.savefig(os.path.join(FIGURE_SAVE_PATH, "Radiation_and_Filter_Nomoto2021.svg"))

# Display the plot
plt.show