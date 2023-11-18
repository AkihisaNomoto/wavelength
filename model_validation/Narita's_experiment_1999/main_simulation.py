import os
import pandas as pd
import matplotlib.pyplot as plt
from model import ReceptorModel
import plot_experimental_conditions as condition
import configration as config

# Constants
DATA_FILE_PATH = "/data/Narita_1999_normalized_spectral_radiance.csv"
plt.rcParams['font.family'] = 'Arial'

# Read the data
df = pd.read_csv(DATA_FILE_PATH)

df.columns = ["wavelength_nm", "Visible (0.30–0.84 µm)", "Near-infrared (0.80 – 1.35 µm)", "Mid-infrared (1.70 – 2.30 µm)"]
df.index = df["wavelength_nm"]
print(type(df["Visible (0.30–0.84 µm)"]))
print(df["Visible (0.30–0.84 µm)"])

#Energy Distribution of Three Types of Radiance
q_total = 1220
t_db = 24.7
t_r = 25.5
t_core = 34.3
hc = 6.4 # convective heat transfer coefficient [W/m2K]
hr = 5.1 # radiative heat transfer coefficient [W/m2K]

result = {}
for rad_name in ["Visible (0.30–0.84 µm)", "Near-infrared (0.80 – 1.35 µm)", "Mid-infrared (1.70 – 2.30 µm)"]:  #[W/m2/10nm]

    model = ReceptorModel()
    model.reset_simulation()

    model.T_core = t_core
    model.hc = hc
    model.hr = hr

    model.q_spectrum = df[rad_name]

    model.add_phase(duration_in_sec=1000, t_db=t_db, t_r=t_r, q_irradiance=0)
    model.add_phase(duration_in_sec=20, t_db=t_db, t_r=t_r, q_irradiance=q_total)

    df_simulation_results = model.simulate(show_input=True)

    csv_path = f"Narita_1999_simulation_results_{rad_name}.csv"
    df_simulation_results.to_csv(os.path.join(config.DATA_DIRECTORY, csv_path))

    result[rad_name] = df_simulation_results.copy()


fig1, axes = plt.subplots(2, 2, figsize=(11, 6.5))

for rad_name in ["Visible (0.30–0.84 µm)", "Near-infrared (0.80 – 1.35 µm)", "Mid-infrared (1.70 – 2.30 µm)"]:
    dfh = result[rad_name].copy()

    marker_size = 5
    linestyle = "dashed"
    marker = "o"

    # axes[0,0] Temperature distribution [oC]
    ser = dfh.loc[dfh.index[-1], "T_0":"T_35"].copy()  # last row
    print(ser)
    ser.index = model.node_coordinates * 10**3  # unit m to mm
    axes[0,0].plot(ser.index, ser, label=rad_name, linestyle=linestyle, marker=marker, markersize=marker_size)
    axes[0, 0].set_xlim((0, 5.4))
    axes[0, 0].set_ylim((31, 34))
    axes[0, 0].set_yticks([31, 32, 33, 34])

    # axes[0,1] Time series of warm receptor temperature [oC]
    ser = dfh.loc[dfh.index[-21:], "T_warm"].copy()
    ser.index = [i for i in range(21)]
    axes[0,1].plot(ser.index, ser, label=rad_name, linestyle=linestyle, marker=marker, markersize=marker_size,)
    axes[0, 1].set_xlim((0, 20))
    axes[0, 1].set_xticks([0, 5, 10, 15, 20])
    axes[0, 1].set_ylim((31, 34))
    axes[0, 1].set_yticks([31, 32, 33, 34])

    # axes[1,0] Absorbed irradiance [W/m2]
    ser = dfh.loc[dfh.index[-2], "q_irradiance_0":"q_irradiance_35"].copy()  # last row
    print(ser)

    ser.index = model.node_coordinates * 10**3  # unit m to mm
    axes[1,0].plot(ser.index, ser, label=rad_name, linestyle=linestyle, marker=marker, markersize=marker_size,)
    axes[1, 0].set_ylim((0, 250))
    axes[1, 0].set_xlim((0, 5.4))
    axes[1, 0].set_xticks([0, 1, 2, 3, 4, 5])

    # axes[1,1] Impulse frequency
    ser = dfh.loc[dfh.index[-21:], "PSI"].copy()
    ser.index = [i for i in range(21)]
    axes[1,1].plot(ser.index, ser, label=rad_name, linestyle=linestyle, marker=marker, markersize=marker_size, alpha=0.5)
    axes[1, 1].set_ylim((0, 5))
    axes[1, 1].set_xlim((0, 20))
    axes[1, 1].set_xticks([0, 5, 10, 15, 20])


# Axes labels
axes[0, 0].set_ylabel("Temperature [°C]")
axes[0, 0].set_xlabel("Distance from core [mm]")
axes[0, 1].set_ylabel("Warm receptor temperature [°C]")
axes[0, 1].set_xlabel("Time [s]")
axes[1, 0].set_ylabel("Absorbed irradiance [W/m$^2$]")
axes[1, 0].set_xlabel("Distance from core [mm]")
axes[1, 1].set_ylabel("Impulse frequency [Hz]")
axes[1, 1].set_xlabel("Time [s]")

# Indicating warm receptor location
for i in [0, 1]:
    axes[i, 0].axvline(4.9, 0, 500, linestyle="dotted", color="grey")
    axes[i, 0].text(0.77, 0.9, "Warm receptor →", transform=axes[i, 0].transAxes,
                    horizontalalignment="center", color="black", fontsize=10)

# Layout adjustments
fig1.tight_layout(rect=[0, 0, 1, 0.96])
fig1.align_labels()

# Adding legend
handles0, labels0 = axes[0, 0].get_legend_handles_labels()
fig1.legend(handles0, labels0, ncol=3, loc="upper center", frameon=False)

# Define labels for the subplots in a 2D array
# Top row: 'a' (left) and 'c' (right)
# Bottom row: 'b' (left) and 'd' (right)
subplot_labels = [['(a)', '(c)'], ['(b)', '(d)']]

# Loop through rows and columns of the axes array
for i, row in enumerate(axes):
    for j, ax in enumerate(row):
        # Place the text slightly outside the upper left corner of the current subplot
        # The exact position may need to be adjusted depending on the subplot's data and limits
        ax.text(0.07, 0.9, subplot_labels[i][j], transform=ax.transAxes,
                fontsize=14, fontweight='bold', va='center', ha='right')

plt.subplots_adjust(wspace=0.2)

# Saving the figure
fig1.savefig(config.FIGURE_PATH + "Narita_1999_simulation_results.svg")
plt.show()

