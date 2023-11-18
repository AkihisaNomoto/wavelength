import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from model import ReceptorModel
import configration as config

# Constants
plt.rcParams["font.family"] = "Arial"
experiments_summary_dict = {
    "Narita_1999": {
        "q_total": 1220,
        "t_db": 24.7,
        "t_r": 25.5,
        "t_core": 34.3,
        "hc": 6.4,
        "hr": 5.1,
        "data_path": config.NARITA_EXP_SPECTRUM_DATA_PATH,
        "rad_names": [
            "Visible (0.30–0.84 µm)",
            "Near-infrared (0.80 – 1.35 µm)",
            "Mid-infrared (1.70 – 2.30 µm)",
        ],
        "figure_configuration": {
            "y_axis_temperature_range": [32, 37],
            "y_axis_absorbed_irradiance_range": [0, 400],
            "y_axis_impulse_frequency_range": [0, 20],
        },
    },
    "Matsui_1986": {
        "q_total": 2000,
        "t_db": 19.5,
        "t_r": 19.5,
        "t_core": 34.3,
        "hc": 4.5,
        "hr": 5.1,
        "data_path": config.MATSUI_EXP_SPECTRUM_DATA_PATH,
        "rad_names": ["A (0.72 - 2.7µm)", "B (1.5 - 4.8µm)", "C (6 - 20µm)"],
        "figure_configuration": {
            "y_axis_temperature_range": [30, 38],
            "y_axis_absorbed_irradiance_range": [0, 2000],
            "y_axis_impulse_frequency_range": [0, 25],
        },
    },
    "Nomoto_2021": {
        "q_a": 228,
        "q_b": 184,
        "q_c": 211,
        "t_db": 25.3,
        "t_r": 25.2,
        "t_core": 33.6,
        "hc": 4.5,
        "hr": 5.1,
        "data_path": config.NOMOTO_EXP_SPECTRUM_DATA_PATH,
        "rad_names": ["A (0.8 - 1.4 µm)", "B (2.3 - 5.0 µm)", "C (2.3 µm upward)"],
        "figure_configuration": {
            "y_axis_temperature_range": [31, 34],
            "y_axis_absorbed_irradiance_range": [0, 250],
            "y_axis_impulse_frequency_range": [0, 5],
        },
    },
}

model = ReceptorModel()


def simulate_experiment_and_get_dataframe(experiments_summary_dict, which_experiment):
    experiment_dict = experiments_summary_dict[which_experiment]
    rad_names = experiment_dict["rad_names"]

    # Read the data
    df = pd.read_csv(experiment_dict["data_path"])

    df.columns = ["wavelength_nm"] + rad_names
    df.index = df["wavelength_nm"]

    result = {}
    for rad_name in rad_names:  # [W/m2/10nm]
        model = ReceptorModel()
        model.reset_simulation()

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
            elif rad_name == "C (2.3 µm upward)":
                model.q_total_irradiance = experiment_dict["q_c"]
        elif which_experiment == "Matsui_1986":
            # It was assumed that the irradiation of 2000 W/m2 included the radiation from the ambient environment,
            # so, ambient radiant temperature is set to -273.15 so that radiant heat transfer to the ambient environment can be set to 0 W/m2.
            model.T_r = -273.15
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

        print(result[rad_name])

    return result


def plot_experiment_results(results, model, experiments_summary_dict, which_experiment):
    fig, axes = plt.subplots(2, 2, figsize=(11, 6.5))

    experiment_dict = experiments_summary_dict[which_experiment]

    for rad_name in results.keys():
        dfh = results[rad_name].copy()

        marker_size = 5
        linestyle = "dashed"
        marker = "o"

        # Temperature distribution
        ser = dfh.loc[dfh.index[-1], "T_0":"T_35"].copy()  # last row
        ser.index = model.node_coordinates * 10**3  # unit m to mm
        axes[0, 0].plot(
            ser.index,
            ser,
            label=rad_name,
            linestyle=linestyle,
            marker=marker,
            markersize=marker_size,
        )
        # x axis
        axes[0, 0].set_xlim((0, 5.4))
        axes[0, 0].set_xticks([0, 1, 2, 3, 4, 5])
        # y axis
        axes[0, 0].set_ylim(
            experiment_dict["figure_configuration"]["y_axis_temperature_range"]
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
            markersize=marker_size,
        )
        # x axis
        axes[0, 1].set_xlim((0, 20))
        axes[0, 1].set_xticks([0, 5, 10, 15, 20])
        # y axis
        axes[0, 1].set_ylim(
            experiment_dict["figure_configuration"]["y_axis_temperature_range"]
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
            markersize=marker_size,
        )
        # x axis
        axes[1, 0].sharex(axes[0, 0])
        # y axis
        axes[1, 0].set_ylim(
            experiment_dict["figure_configuration"]["y_axis_absorbed_irradiance_range"]
        )

        # Impulse frequency
        ser = dfh.loc[dfh.index[-21:], "PSI"].copy()
        ser.index = [i for i in range(21)]
        axes[1, 1].plot(
            ser.index,
            ser,
            label=rad_name,
            linestyle=linestyle,
            marker=marker,
            markersize=marker_size,
            alpha=0.5,
        )
        # x axis
        axes[1, 1].sharex(axes[0, 1])
        # y axis
        axes[1, 1].set_ylim(
            experiment_dict["figure_configuration"]["y_axis_impulse_frequency_range"]
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
        axes[i, 0].axvline(4.9, 0, 500, linestyle="dotted", color="grey")
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
    subplot_labels = [["(a)", "(c)"], ["(b)", "(d)"]]
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            ax.text(
                0.07,
                0.9,
                subplot_labels[i][j],
                transform=ax.transAxes,
                fontsize=14,
                fontweight="bold",
                va="center",
                ha="right",
            )

    plt.subplots_adjust(wspace=0.2)

    # Saving the figure
    fig.savefig(
        os.path.join(
            config.FIGURE_DIRECTORY, f"{which_experiment}_simulation_results.svg"
        )
    )
    plt.show()


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