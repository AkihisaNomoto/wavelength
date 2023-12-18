import pandas as pd
import matplotlib.pyplot as plt
import os

import configration as config
# Set global matplotlib parameters for font
plt.rcParams['font.family'] = 'Arial'


# Define constants
DATA_FILE_PATH = (
    "C:\\Users\\monyo\\PycharmProjects\\wavelength\\data\\skin-spectral-properties.csv"
)
SELECTED_WAVELENGTHS_BELOW_2_5_UM = [
    300,
    350,
    370,
    400,
    450,
    500,
    550,
    600,
    650,
    700,
    750,
    800,
    900,
    1000,
    1100,
    1200,
    1300,
    1400,
    1500,
    1600,
    1800,
    2000,
    2200,
    2400
]

df_all = pd.read_csv(DATA_FILE_PATH)

# Fig_Spectral Absorption and Scattering Coefficients in Skin Surface[1/mm]
fig, axes = plt.subplots(2, 1, sharex=True, figsize=(6, 6))

# Get EXP data and plot（below 2.5µm）
df_all.index = df_all["wavelength_nm"]
df = df_all.query(
    f"index == {SELECTED_WAVELENGTHS_BELOW_2_5_UM}"
)
# data in coloums
wavelength = df["wavelength_nm"].values * 10**-3 # from nm to µm
reflectance_series = df["reflectance_nd"].values
transmittance_series = df["transmittance_nd"].values
absorption_coefficient_series = df["absorption_coefficient_1/mm"].values
scattering_coefficient_series = df["scattering_coefficient_1/mm"].values

# plot data
axes[0].plot(
    wavelength,
    reflectance_series,
    label="$R_λ$",
    linestyle="dashed",
    marker="o",
    color="black",
    markerfacecolor="black",
    alpha=0.5,
)
axes[0].plot(
    wavelength,
    transmittance_series,
    label="$T_λ$",
    linestyle="dashed",
    marker="o",
    color="black",
    markerfacecolor="white",
    alpha=0.5,
)
axes[1].plot(
    wavelength,
    absorption_coefficient_series,
    label="$K_λ$",
    linestyle="dashed",
    marker="o",
    color="black",
    markerfacecolor="black",
    alpha=0.5,
)
axes[1].plot(
    wavelength,
    scattering_coefficient_series,
    label="$S_λ$",
    linestyle="dashed",
    marker="o",
    color="black",
    markerfacecolor="white",
    alpha=0.5,
)

# 2.5µm以上描写
df = df_all.query("wavelength_nm > 2400")
wavelength = df["wavelength_nm"].values * 10**-3
reflectance_series = df["reflectance_nd"].values
transmittance_series = df["transmittance_nd"].values
absorption_coefficient_series = df["absorption_coefficient_1/mm"].values
scattering_coefficient_series = df["scattering_coefficient_1/mm"].values

axes[0].plot(wavelength, reflectance_series, linestyle="dashed", color="black", alpha=0.5)
axes[0].plot(wavelength, transmittance_series, linestyle="dashed", color="black", alpha=0.5)
axes[1].plot(wavelength, absorption_coefficient_series, linestyle="dashed", color="black", alpha=0.5)
axes[1].plot(wavelength, scattering_coefficient_series, linestyle="dashed", color="black", alpha=0.5)

# Text
axes[0].axhspan(ymin=0.9, ymax=1.0, color="lightgray", alpha=0.3)
y_text_position = 0.925
bands = [("Ultraviolet", 0.20), ("Visible", 0.56), ("Near-IR", 1.05), ("Mid-IR", 2.05), ("Far-IR", 8.0)]
for band, x_position in bands:
    axes[0].text(x_position, y_text_position, band, ha="center", fontsize=10)
axes[0].set_xticks([0.3, 0.8, 1.4, 3.0, 20])

# Loop through each of the two subplots to add vertical lines at specified wavelengths
for i in [0, 1]:
    # Define the wavelengths at which vertical lines will be added
    for x in [0.4, 0.8, 1.4, 3.0]:
        # This visually indicates divisions between different spectral regions (e.g., UV, visible, etc.)
        axes[i].axvline(x, 0, 1, linestyle="dotted", color="lightgrey")

# Set legend, scale, limits, labels and tick parameters for axes[0] (reflectance and transmittance)
axes[0].legend(bbox_to_anchor=(0, 0.93), loc="upper left", borderaxespad=1)
axes[0].set_xscale("log")
axes[0].set_xlim((0.1, 25))
axes[0].set_ylim((0, 1))
axes[0].set_ylabel("$R_λ$, $T_λ$ [-]")
axes[0].tick_params(which="major", length=5)
axes[0].tick_params(which="minor", length=2.5)

# Set legend, scale, limits, labels and tick parameters for axes[1] (absorption and scattering)
# Get handles and labels to switch the order of legends if necessary
handles, labels = axes[1].get_legend_handles_labels()
axes[1].legend(
    handles,
    labels,
    bbox_to_anchor=(0, 1),
    loc="upper left",
    borderaxespad=1,
)
axes[1].set_xlim((0.1, 25))
axes[1].set_xscale("log")
axes[1].set_yscale("log")
axes[1].tick_params(which="major", length=5)
axes[1].tick_params(which="minor", length=2.5)
axes[1].set_ylabel("$K_λ$, $S_λ$ [mm$\mathregular{^{-1}}$]")
axes[1].set_xlabel("Wavelength [μm]")

# Define the labels for the subplots
subplot_labels = ['a', 'b']
# Loop through each subplot to add the labels 'a)' and 'b)'
for i, ax in enumerate(axes):
    # Place the text slightly outside the upper left corner of the current subplot
    # The exact position may need to be adjusted depending on the subplot's data and limits
    ax.text(-0.1, 1.0, subplot_labels[i], transform=ax.transAxes, fontsize=14, fontweight='bold', va='center', ha='right')

fig.tight_layout()
fig.align_labels()
plt.savefig(os.path.join(config.FIGURE_DIRECTORY,"Spectral radiative properties of the skin (Japanese).svg"))
plt.show()



