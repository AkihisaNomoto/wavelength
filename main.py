import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from model import ReceptorModel
import configration as config

# Constants
plt.rcParams["font.family"] = "Arial"
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.get_cmap("Set1").colors)
run_detail_simulation = False

# Define summary dictionary including experimental infomation
experiments_summary_dict = {
    "Narita_1999": {
        "q_total": 1220,
        "t_db": 24.7,
        "t_r": 25.5,
        "t_core": 35.9,
        "hc": 6.4,
        "hr": 5.1,
        "data_path": config.NARITA_EXP_SPECTRUM_DATA_PATH,
        "rad_names": [
            "Visible (0.30–0.84 µm)",
            "Near-infrared (0.80 – 1.35 µm)",
            "Mid-infrared (1.70 – 2.30 µm)",
        ],
        "figure_configuration": {
            "y_axis_temperature_range": [34, 38],
            "y_axis_temperature_ticks": list(range(34, 39, 1)),
            "y_axis_absorbed_irradiance_range": [0, 400],
            "y_axis_absorbed_irradiance_ticks": list(range(0, 500, 100)),
            "y_axis_impulse_frequency_range": [0, 20],
            "y_axis_impulse_frequency_ticks": list(range(0, 25, 5)),
        },
    },
    "Matsui_1986": {
        "q_total": 2000,
        "t_db": 19.5,
        "t_r": 19.5,
        "t_core": 32.5,
        "hc": 4.5,
        "hr": 5.1,
        "data_path": config.MATSUI_EXP_SPECTRUM_DATA_PATH,
        "rad_names": [
            "Near- to mid-infrared  (0.72 - 2.7µm)",
            "Mid- to far-infrared (1.5 - 4.8µm)",
            "Far-infrared  (6 - 20µm)",
        ],
        "figure_configuration": {
            "y_axis_temperature_range": [30, 40],
            "y_axis_temperature_ticks": list(range(30, 41, 2)),
            "y_axis_absorbed_irradiance_range": [0, 2000],
            "y_axis_absorbed_irradiance_ticks": list(range(0, 2500, 500)),
            "y_axis_impulse_frequency_range": [0, 25],
            "y_axis_impulse_frequency_ticks": list(range(0, 30, 5)),
        },
    },
    "Nomoto_2021": {
        "q_a": 228,
        "q_b": 184,
        "q_c": 211,
        "t_db": 25.3,
        "t_r": 25.2,
        "t_core": 35.5,
        "hc": 4.5,
        "hr": 5.1,
        "data_path": config.NOMOTO_EXP_SPECTRUM_DATA_PATH,
        "rad_names": [
            "A (0.8 - 1.4 µm)",
            "B (2.3 - 5.0 µm)",
            "C (2.3 µm and above)",
        ],
        "figure_configuration": {
            "y_axis_temperature_range": [33, 36],
            "y_axis_temperature_ticks": list(range(33, 37, 1)),
            "y_axis_absorbed_irradiance_range": [0, 250],
            "y_axis_absorbed_irradiance_ticks": list(range(0, 300, 50)),
            "y_axis_impulse_frequency_range": [0, 8],
            "y_axis_impulse_frequency_ticks": list(range(0, 9, 2)),
        },
    },
}
detailed_wavelength_analysis_dict = {
    "q_total": 100,
    "t_db": 24.7,
    "t_r": 25.5,
    "t_core": 34.3,
    "hc": 6.4,
    "hr": 5.1,
    "data_path": config.NARITA_EXP_SPECTRUM_DATA_PATH,
    "wavelengths": list(range(300, 20001, 100)),
}


def conduct_detailed_wavelength_simulation():
    result = {}
    psi = []
    for wavelength in detailed_wavelength_analysis_dict["wavelengths"]:  # [W/m2/10nm]
        # Define receptor model instance
        model = ReceptorModel()

        # Set experimental conditions
        model._reset_simulation()
        model.T_core = detailed_wavelength_analysis_dict["t_core"]
        model.hc = detailed_wavelength_analysis_dict["hc"]
        model.hr = detailed_wavelength_analysis_dict["hr"]
        model.T_db = detailed_wavelength_analysis_dict["t_db"]
        model.T_r = detailed_wavelength_analysis_dict["t_r"]
        model.q_total_irradiance = 100
        # Create a Series with 1 for rad_name and 0 for others in "spectral irradiance"
        model.q_spectrum = pd.Series(
            [1 if name == wavelength else 0 for name in model.wavelengths],
            index=model.wavelengths,
        )
        print(model.q_spectrum)

        # Initialize the model by running a long time
        model.add_phase(
            duration_in_sec=1000,
            t_db=model.T_db,
            t_r=model.T_r,
            q_irradiance=0,
        )

        # Add irradiation period
        model.add_phase(
            duration_in_sec=20,
            t_db=model.T_db,
            t_r=model.T_r,
            q_irradiance=round(model.q_total_irradiance, 2),
        )
        # Define simulation results
        df_simulation_results = model.simulate(show_input=True)

        ser = df_simulation_results["PSI"][-21:]
        ser = ser.mean()
        psi.append(ser)

    df = pd.DataFrame({"PSI": psi})
    df["Ratio"] = df["PSI"] / df["PSI"].max()

    df.index.name = "wavelength_µm"

    wavelengths_array = np.array(detailed_wavelength_analysis_dict["wavelengths"])
    df.index = wavelengths_array * 10**-3  # convert nm to µm

    # Save as CSV file
    title = "wavelength_dependence_from_0.3_to_20_µm"
    csv_path = title + ".csv"
    df.to_csv(os.path.join(config.DATA_DIRECTORY, csv_path))

    # Plot
    plt.figure(figsize=(6, 3.5))

    for x in [0.4, 0.8, 1.4, 3.0]:
        plt.axvline(x, 0, 1, linestyle="dotted", color="lightgrey")

    plt.plot(
        df.index,
        df["Ratio"],
        marker="o",
        color="black",
        markerfacecolor="black",
        linestyle="dashed",
        alpha=0.5,
    )
    plt.tight_layout()
    plt.xticks([0, 100, 1000, 10000])
    plt.xlabel("Wavelength [µm]")
    plt.ylabel("PSI ratio [-]")
    plt.xscale("log")
    plt.xlim([0.1, 25])
    plt.ylim([0, 1])

    plt.axhspan(0, 0.1, color="lightgray", alpha=0.3)
    plt.tick_params(pad=6)
    plt.text(
        0.20, 0.03, "Ultraviolet", horizontalalignment="center", c="black", fontsize=10
    )  # visible
    plt.text(
        0.56, 0.03, "Visible", horizontalalignment="center", c="black", fontsize=10
    )  # visible
    plt.text(
        1.05, 0.03, "Near-IR", horizontalalignment="center", c="black", fontsize=10
    )  # near-IR
    plt.text(
        2.0, 0.03, "Mid-IR", horizontalalignment="center", c="black", fontsize=10
    )  # mid-IR
    plt.text(
        8.0, 0.03, "Far-IR", horizontalalignment="center", c="black", fontsize=10
    )  # far-IR

    plt.tight_layout()
    fig_path = title + ".svg"
    plt.savefig(os.path.join(config.FIGURE_DIRECTORY, fig_path))


def simulate_experiment_and_get_dataframe(experiments_summary_dict, which_experiment):
    # Get an experimental information from summary dictionary
    experiment_dict = experiments_summary_dict[which_experiment]

    # Get rad name
    rad_names = experiment_dict["rad_names"]

    # Define spectral irradiation data
    df = pd.read_csv(experiment_dict["data_path"])
    df.columns = ["wavelength_nm"] + rad_names
    df.index = df["wavelength_nm"]

    result = {}
    psi = []
    # Iterate by radiation spectrum
    for rad_name in rad_names:  # [W/m2/10nm]
        # Define receptor model instance
        model = ReceptorModel()

        # Set experimental conditions
        model._reset_simulation()
        model.T_core = experiment_dict["t_core"]
        model.hc = experiment_dict["hc"]
        model.hr = experiment_dict["hr"]
        model.T_db = experiment_dict["t_db"]
        model.T_r = experiment_dict["t_r"]
        model.q_total_irradiance = 0
        model.q_spectrum = df[rad_name]

        # Initialize the model by running a long time
        model.add_phase(
            duration_in_sec=1000,
            t_db=model.T_db,
            t_r=model.T_r,
            q_irradiance=model.q_total_irradiance,
        )

        # Conditional input
        if which_experiment == "Nomoto_2021":
            # Measured irradiance is used for simulating Nomoto's experiment
            if rad_name == "A (0.8 - 1.4 µm)":
                model.q_total_irradiance = experiment_dict["q_a"]
            elif rad_name == "B (2.3 - 5.0 µm)":
                model.q_total_irradiance = experiment_dict["q_b"]
            elif rad_name == "C (2.3 µm and above)":
                model.q_total_irradiance = experiment_dict["q_c"]
        elif which_experiment == "Matsui_1986":
            # It was assumed that the irradiation of 2000 W/m2 included the radiation from the ambient environment,
            # so, ambient radiant temperature is set to -273.15 so that radiant heat transfer to the ambient environment can be set to 0 W/m2.
            model.q_radiation = 0
            model.q_total_irradiance = experiment_dict["q_total"]
        else:
            # Since Naria's experiment focuses on solar radiation, longwave radiation heat transfer happens.
            # Only parameter to change is external heat load by irradiance.
            model.q_total_irradiance = experiment_dict["q_total"]

        # Add irradiation period
        model.add_phase(
            duration_in_sec=20,
            t_db=model.T_db,
            t_r=model.T_r,
            q_irradiance=model.q_total_irradiance,
        )

        # Define simulation results
        df_simulation_results = model.simulate(show_input=True)

        # Save as CSV file
        csv_path = f"{which_experiment}_simulation_results_{rad_name}.csv"
        df_simulation_results.to_csv(os.path.join(config.DATA_DIRECTORY, csv_path))

        # Summarize results
        result[rad_name] = df_simulation_results.copy()

        # Calculate PSI ratio as max value is 1
        ser = result[rad_name]["PSI"].copy()
        ser = ser[-21:]
        ser = round(ser.sum(), 0)
        psi.append(ser)
    print("PSI", psi)
    print("PSI ratio", psi / max(psi))

    return result


def plot_experiment_results(results, model, experiments_summary_dict, which_experiment):
    fig, axes = plt.subplots(2, 2, figsize=(11, 6.5))

    experiment_dict = experiments_summary_dict[which_experiment]

    # Define color mapping
    colors = ["red", "blue", "green"]

    for i, rad_name in enumerate(results.keys()):
        dfh = results[rad_name].copy()

        # Define figure configuration
        marker_size = 4
        linestyle = "solid"
        marker = "o"
        alpha = 1
        makerface_color = "white"
        # color = colors[i % len(colors)]

        # Temperature distribution
        ser = dfh.loc[dfh.index[-1], "T_0":"T_35"].copy()  # last row
        ser.index = model.node_coordinates * 10**3  # unit m to mm
        axes[0, 0].plot(
            ser.index,
            ser,
            label=rad_name,
            linestyle=linestyle,
            marker=marker,
            markerfacecolor=makerface_color,
            markersize=marker_size,
            alpha=alpha,
            # color=color,
        )
        # x axis
        axes[0, 0].set_xlim((0, 5.4))
        axes[0, 0].set_xticks([0, 1, 2, 3, 4, 5])
        # y axis
        axes[0, 0].set_ylim(
            experiment_dict["figure_configuration"]["y_axis_temperature_range"]
        )
        axes[0, 0].set_yticks(
            experiment_dict["figure_configuration"]["y_axis_temperature_ticks"]
        )

        # Time series of warm receptor temperature
        ser = dfh.loc[dfh.index[-21:], "T_warm"].copy()
        ser.index = [i for i in range(21)]
        axes[0, 1].plot(
            ser.index,
            ser,
            label=rad_name,
            linestyle=linestyle,
            marker=marker,
            markerfacecolor=makerface_color,
            markersize=marker_size,
            alpha=alpha,
            # color=color,
        )
        # x axis
        axes[0, 1].set_xlim((0, 20))
        axes[0, 1].set_xticks([0, 5, 10, 15, 20])
        # y axis
        axes[0, 1].set_ylim(
            experiment_dict["figure_configuration"]["y_axis_temperature_range"]
        )
        axes[0, 1].set_yticks(
            experiment_dict["figure_configuration"]["y_axis_temperature_ticks"]
        )

        # Absorbed irradiance
        ser = dfh.loc[
            dfh.index[-2], "q_irradiance_0":"q_irradiance_35"
        ].copy()  # last row
        ser.index = model.node_coordinates * 10**3  # unit m to mm
        axes[1, 0].plot(
            ser.index,
            ser,
            label=rad_name,
            linestyle=linestyle,
            marker=marker,
            markerfacecolor=makerface_color,
            markersize=marker_size,
            alpha=alpha,
            # color=color,
        )
        # x axis
        axes[1, 0].sharex(axes[0, 0])
        # y axis
        axes[1, 0].set_ylim(
            experiment_dict["figure_configuration"]["y_axis_absorbed_irradiance_range"]
        )
        axes[1, 0].set_yticks(
            experiment_dict["figure_configuration"]["y_axis_absorbed_irradiance_ticks"]
        )

        # Impulse frequency
        ser = dfh.loc[dfh.index[-21:], "R"].copy()
        ser.index = [i for i in range(21)]
        axes[1, 1].plot(
            ser.index,
            ser,
            label=rad_name,
            linestyle=linestyle,
            marker=marker,
            markersize=marker_size,
            markerfacecolor=makerface_color,
            alpha=alpha,
            # color=color,
        )
        # x axis
        axes[1, 1].sharex(axes[0, 1])
        # y axis
        axes[1, 1].set_ylim(
            experiment_dict["figure_configuration"]["y_axis_impulse_frequency_range"]
        )
        axes[1, 1].set_yticks(
            experiment_dict["figure_configuration"]["y_axis_impulse_frequency_ticks"]
        )

    # Set labels and layout
    axes[0, 0].set_ylabel("Temperature [°C]")
    axes[0, 0].set_xlabel("Distance from core [mm]")
    axes[0, 1].set_ylabel("Warm receptor temperature [°C]")
    axes[0, 1].set_xlabel("Time [s]")
    axes[1, 0].set_ylabel("Absorbed irradiance [W/m$^2$]")
    axes[1, 0].set_xlabel("Distance from core [mm]")
    axes[1, 1].set_ylabel("Impulse frequency [Hz]")
    axes[1, 1].set_xlabel("Time [s]")

    # Indicating warm receptor location and layout adjustments
    for i in [0, 1]:
        axes[i, 0].axvline(4.9, 0, 500, linestyle="dotted", color="black")
        axes[i, 0].text(
            0.77,
            0.9,
            "Warm receptor →",
            transform=axes[i, 0].transAxes,
            horizontalalignment="center",
            color="black",
            fontsize=10,
        )

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.align_labels()

    # Adding legend and subplot labels
    handles0, labels0 = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles0, labels0, ncol=3, loc="upper center", frameon=False)
    subplot_labels = [["a", "c"], ["b", "d"]]
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            ax.text(
                0.07,
                0.9,
                subplot_labels[i][j],
                transform=ax.transAxes,
                fontsize=16,
                fontweight="bold",
                va="center",
                ha="right",
            )

    plt.subplots_adjust(wspace=0.2)

    # Saving the figure
    file_extensions = [".svg", ".png"]
    for extension in file_extensions:
        fig.savefig(
            os.path.join(
                config.FIGURE_DIRECTORY,
                f"{which_experiment}_simulation_results{extension}",
            )
        )
    # plt.show()


if __name__ == "__main__":
    model = ReceptorModel()
    for experiment_name in experiments_summary_dict.keys():
        rad_names = experiments_summary_dict[experiment_name]["rad_names"]
        result = simulate_experiment_and_get_dataframe(
            experiments_summary_dict=experiments_summary_dict,
            which_experiment=experiment_name,
        )
        plot_experiment_results(
            results=result,
            model=model,
            experiments_summary_dict=experiments_summary_dict,
            which_experiment=experiment_name,
        )
    if run_detail_simulation == True:
        conduct_detailed_wavelength_simulation()
