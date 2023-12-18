import numpy as np
import pandas as pd
import pythermalcomfort.models.jos3
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
from pythermalcomfort.models import JOS3
from pythermalcomfort.jos3_functions.parameters import Default

# Define constants
DATA_FILE_PATH = (
    "C:\\Users\\monyo\\PycharmProjects\\wavelength\\data\\skin-spectral-properties.csv"
)
df = pd.read_csv(DATA_FILE_PATH)

# Get EXP data and plot（below 2.5µm）
df.index = df["wavelength_nm"]
# data in coloums
wavelength = df["wavelength_nm"] * 10**-3  # from nm to µm


class ReceptorModel:
    """
    A model representing the thermal response of skin receptors.

    This class simulates the response of skin receptors to varying thermal environments.
    It takes into account the conduction, convection, and radiation heat transfer
    processes, as well as the distribution of radiation within skin layers.
    """

    def __init__(self):
        # Basic physical properties of the skin
        self.length = 5.4e-3  # thickness of skin layer [m]
        self.n = 36  # number of discretized skin layers
        self.dt = 0.05  # time step for the simulation [s]

        # Initial conditions for the simulation
        self.simulation_time = 0  # cumulative simulation time [s]
        self.initial_temperature = 34  # initial temperature of skin layers [°C]
        self.T = (
            np.ones(self.n) * self.initial_temperature
        )  # temperature distribution across layers

        # Core and environmental temperatures
        self.T_core = 36.9  # core body temperature [°C]
        self.T_db = 25  # dry bulb (ambient) te   mperature [°C]
        self.T_r = 25  # radiant temperature [°C]

        # Irradiance related properties
        self.q_total_irradiance = 0  # total irradiance [W/m²]
        self.wavelengths = np.arange(
            300, 50001, 10
        )  # wavelengths from 300nm to 50000nm
        self.q_spectrum = pd.Series(
            np.zeros(len(self.wavelengths)), index=self.wavelengths
        )  # spectral irradiance

        # Heat transfer coefficients
        self.hc = 4  # convection heat transfer coefficient [W/m²K]
        self.hr = 5  # radiation heat transfer coefficient [W/m²K]

        # Receptor calculation
        self.coef_static_warm_receptor = 2  # Hz/K
        self.coef_static_cold_receptor = -2  # Hz/K
        self.coef_dynamic_warm_receptor = 56  # Hz·s/K
        self.coef_dynamic_cold_receptor = -62  # Hz·s/K
        self.T_no_static_discharge = 33

        # Initialize additional parameters
        self._initialize_parameters()

        # Simulation results and phases
        self.simulation_results = {}  # dict results of the simulation
        self.phases = []  # list to store different simulation phases

    def _initialize_parameters(self):
        """
        Initialize additional parameters needed for the simulation.
        This includes calculations for heat transfer, diffusivity,
        resistance, and absorption properties.
        """
        # Heat transfer coefficient, layer thickness, and coordinates
        self.h = self.hc + self.hr  # total heat transfer coefficient [W/m²K]
        self.dx = self.length / self.n  # thickness of each skin layer [m]
        self.node_coordinates = np.linspace(
            self.dx / 2, self.length - self.dx / 2, self.n
        )  # coordinates of each layer [m]

        # Heat capacity and conductance
        self.capacity = 4.3e6 * self.dx  # heat capacity [J/m²K]
        self.conductance = 0.25  # heat conductance [W/mK]
        self.diffusivity = 1 / (
            self.dx / self.conductance * self.capacity
        )  # thermal diffusivity [m²/s]

        # Thermal resistances
        self.r_skin2core = self.dx / (2 * self.conductance)  # skin to core [m²K/W]
        self.r_skin2skin = (
            self.dx / self.conductance
        )  # skin layer to skin layer [m²K/W]
        self.r_skin2amb_convection = (
            self.dx / (2 * self.conductance) + 1 / self.hc
        )  # skin to ambient [m²K/W]
        self.r_skin2amb_radiation = (
            self.dx / (2 * self.conductance) + 1 / self.hr
        )  # skin to ambient [m²K/W]

        # Absorption rates for different wavelengths
        self.absorption_sw = 0.70  # short wavelength absorption rate
        self.absorption_lw = 0.97  # long wavelength absorption rate

        # Stefan-Boltzmann constant
        self.sigma = 5.67e-8  # [W/m²K⁴]

    def _set_skin_properties(self, df):
        """
        Set skin properties from a provided DataFrame and align them with the wavelengths in self.q_spectrum.

        Parameters:
        - df (DataFrame): A DataFrame containing spectral properties of the skin.
        """
        # Ensure the spectral properties align with the wavelengths
        self.spectral_reflectance = df["reflectance_nd"].reindex(
            self.wavelengths, fill_value=0
        )
        self.spectral_transmittance = df["transmittance_nd"].reindex(
            self.wavelengths, fill_value=0
        )
        self.spectral_absorption_coefficient = df[
            "absorption_coefficient_1/mm"
        ].reindex(self.wavelengths, fill_value=0)
        self.spectral_scattering_coefficient = df[
            "scattering_coefficient_1/mm"
        ].reindex(self.wavelengths, fill_value=0)

    def _replace_nan_with_zero(self, lst):
        """
        Replace NaN values in a list with zeros.

        Parameters:
        - lst (list): A list that may contain NaN values.

        Returns:
        - list: The input list with NaN values replaced by zeros.
        """
        arr = np.array(lst)
        arr[np.isnan(arr)] = 0
        return arr.tolist()

    def add_phase(self, duration_in_sec, t_db, t_r, q_irradiance):
        """
        Add a simulation phase with specific environmental conditions.

        Parameters:
        - duration_in_sec (int): Duration of the phase in seconds.
        - t_db (float): Dry bulb temperature (°C).
        - t_r (float): Radiant temperature (°C).
        - q_irradiance (float): Total irradiance (W/m²).

        Raises:
        - ValueError: If any parameter is out of a reasonable range.
        """
        # Validate input parameters
        if duration_in_sec <= 0:
            raise ValueError("Duration must be positive.")
        if q_irradiance < 0:
            raise ValueError("q_irradiance must be non-negative.")

        # Add the phase to the simulation
        self.phases.append(
            {
                "duration_in_sec": duration_in_sec,
                "t_db": t_db,
                "t_r": t_r,
                "q_irradiance": q_irradiance,
            }
        )

    def _reset_simulation(self):
        """
        Reset the simulation to its initial state.
        """
        # Resetting simulation time and temperature distribution
        self.simulation_time = 0
        self.T = np.ones(self.n) * self.initial_temperature

        # Clearing all phases
        self.phases = []

    def _update_environmental_conditions(self, phase):
        """
        Update the environmental conditions based on a given phase.

        Parameters:
        - phase (dict): A dictionary containing environmental conditions for a phase.
        """
        # Update temperatures and irradiance based on the current phase
        self.T_db = phase["t_db"]
        self.T_r = phase["t_r"]
        self.q_total_irradiance = phase["q_irradiance"]

    def _calculate_radiation_distribution(self):
        """
        Calculate the distribution of radiation within the skin layers based on
        spectral irradiance and the optical properties of the skin.

        Returns:
        - numpy.ndarray: An array representing the distribution of radiation across the skin layers.
        """
        # Set skin properties
        self.properties = self._set_skin_properties(df=df)

        # Calculate the irradiance at each node
        self.q_spectral_irradiance = self.q_total_irradiance * self.q_spectrum

        if isinstance(self.q_spectral_irradiance, np.ndarray):
            self.q_spectral_irradiance = pd.Series(
                self.q_spectral_irradiance, index=self.q_spectrum.index
            )

        self.q_irradiance_nodes = []
        for x_cord in self.node_coordinates:
            irradiance_at_node = (
                self.q_spectral_irradiance
                * (1 - self.spectral_reflectance)
                * (
                    np.exp(
                        -(
                            self.spectral_absorption_coefficient
                            + self.spectral_scattering_coefficient
                        )
                        * (x_cord - self.dx / 2)
                        * 1e3
                    )
                    - np.exp(
                        -(
                            self.spectral_absorption_coefficient
                            + self.spectral_scattering_coefficient
                        )
                        * (x_cord + self.dx / 2)
                        * 1e3
                    )
                )
            )
            # irradiance_at_node = (
            #     irradiance_at_node + irradiance_at_node * self.dt / self.capacity
            # )
            self.q_irradiance_nodes.append(irradiance_at_node.sum())

        # Reverse the array to align with the core side
        self.q_distribution_nodes = np.array(self.q_irradiance_nodes[::-1])
        return self.q_distribution_nodes

    def _calculate_heat_flux(self, T):
        """
        Calculate the heat flux for each skin layer.

        Parameters:
        - T (numpy.ndarray): Array of temperatures for each skin layer.

        Returns:
        - numpy.ndarray: Array of heat flux for each skin layer.
        """
        q_total_flux = np.zeros(self.n)

        # Heat balance equations except the boundaries
        for i in range(1, self.n - 1):
            q_total_flux[i] = (
                (T[i - 1] - T[i]) / self.r_skin2skin
                + (T[i + 1] - T[i]) / self.r_skin2skin
                + self.q_irradiance_nodes[i]
            )

        # Equations at the boundaries
        q_total_flux[0] = (
            (T[1] - T[0]) / self.r_skin2skin
            + (self.T_core - T[0]) / self.r_skin2core
            + self.q_irradiance_nodes[0]
        )

        self.q_convection = (self.T_db - T[self.n - 1]) / self.r_skin2amb_convection
        # self.q_radiation = (self.T_r - T[self.n - 1]) / self.r_skin2amb_radiation
        self.q_radiation = (
            self.sigma * self.absorption_lw * (self.T_r + 273.15) ** 4
            - self.sigma * self.absorption_lw * (T[self.n - 1] + 273.15) ** 4
        )
        q_total_flux[self.n - 1] = (
            (T[self.n - 2] - T[self.n - 1]) / self.r_skin2skin
            + self.q_convection
            + self.q_radiation
            + self.q_irradiance_nodes[self.n - 1]
        )

        return q_total_flux

    def _prepare_dataframe(
        self, T_history, q_irradiance_history, input_conditions, show_input
    ):
        """
        Prepare a DataFrame containing the simulation results.

        Parameters:
        - T_history (list): List containing the history of temperatures.
        - q_irradiance_history (list): List containing the history of irradiance nodes.
        - input_conditions (list): List containing the input conditions.
        - show_input (bool): Indicates whether to include input conditions in the DataFrame.

        Returns:
        - pd.DataFrame: DataFrame containing the simulation results.
        """
        # Create DataFrame from temperature history
        columns = ["Current_Time", "dt"] + ["T_" + str(i) for i in range(self.n)]
        df = pd.DataFrame(T_history, columns=columns)

        # Additional Calculations
        df["T_warm"] = (df["T_33"] + 5 * df["T_32"]) / 6  # Warm receptor temperature
        df["dT_warm"] = (
            df["T_warm"].diff() * self.dt
        )  # Derivative of warm receptor temperature
        df["R"] = (
            self.coef_static_warm_receptor
            * np.maximum(0, df["T_warm"] - self.T_no_static_discharge)
            + self.coef_dynamic_warm_receptor * (df["dT_warm"]) / self.dt
        )  # Thermal response
        df["dR"] = df["R"].diff()  # Derivative of thermal response
        time_to_integrate = 20
        df["PSI"] = (
            df["dR"].rolling(int(time_to_integrate / self.dt)).sum()
        )  # Integral of dRt over a window

        # Include input conditions if requested
        if show_input:
            input_df = pd.DataFrame(
                input_conditions,
                columns=["T_core", "T_db", "T_r", "q_total_irradiance"],
            )
            df = pd.concat([df, input_df], axis=1)

            q_irradiance_columns = ["q_irradiance_" + str(i) for i in range(self.n)]
            q_irradiance_df = pd.DataFrame(
                q_irradiance_history, columns=q_irradiance_columns
            )
            df = pd.concat([df, q_irradiance_df], axis=1)

        return df

    def simulate(self, show_input=False):
        """
        Simulate the thermal response of skin receptors over defined phases.

        Parameters:
        - show_input (bool): If True, include input conditions in the output DataFrame.

        Returns:
        - pd.DataFrame: A DataFrame containing the simulation results, including temperatures and thermal responses.

        Raises:
        - ValueError: If no phases have been added before simulation.
        """
        # Check if at least one phase is added
        if not self.phases:
            raise ValueError("At least one phase must be added before simulation.")

        # Initialize variables for simulation
        T = np.ones(self.n) * self.initial_temperature
        T_history = []  # Store temperature history
        q_irradiance_history = []  # Store irradiance history if show_input is True
        input_conditions = []  # Store input conditions if show_input is True
        current_time = 0  # Track current time in the simulation

        # Record initial conditions
        T_history.append(np.append([current_time, self.dt], T.copy()))

        # Iterate over each phase
        for phase in self.phases:
            self._update_environmental_conditions(phase)
            self.q_irradiance_nodes = self._calculate_radiation_distribution()

            # Number of iterations for the current phase
            iteration_number = int(phase["duration_in_sec"] / self.dt)
            for _ in range(iteration_number + 1):
                # Calculate heat flux for each layer
                q_total_flux = self._calculate_heat_flux(T)

                # Update temperatures based on heat flux
                T += q_total_flux * self.dt / self.capacity
                current_time += self.dt

                # Record data at regular intervals
                if current_time % 1.0 < self.dt:
                    T_history.append(np.append([int(current_time), self.dt], T.copy()))

                    if show_input:
                        q_irradiance_history.append(self.q_irradiance_nodes.copy())
                        input_conditions.append(
                            [self.T_core, self.T_db, self.T_r, self.q_total_irradiance]
                        )

        # Convert simulation data to DataFrame
        df = self._prepare_dataframe(
            T_history, q_irradiance_history, input_conditions, show_input
        )
        return df


# Sample usage
if __name__ == "__main__":
    model = ReceptorModel()
    model.add_phase(duration_in_sec=10, t_db=20, t_r=25, q_irradiance=0)
    model.add_phase(duration_in_sec=10, t_db=30, t_r=27, q_irradiance=0)
    simulation_results = model.simulate()
