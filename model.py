import numpy as np
import pandas as pd
from pythermalcomfort.models import JOS3

# Define constants
DATA_FILE_PATH = (
    "C:\\Users\\monyo\\PycharmProjects\\wavelength\\data\\skin-spectral-properties.csv"
)
df = pd.read_csv(DATA_FILE_PATH)

# Get EXP data and plot（below 2.5µm）
df.index = df["wavelength_nm"]
# data in coloums
wavelength = df["wavelength_nm"].values * 10**-3  # from nm to µm
spectral_reflectance = df["reflectance_nd"].values
spectral_transmittance = df["transmittance_nd"].values
spectral_absorption_coefficient = df["absorption_coefficient_1/mm"].values
spectral_scattering_coefficient = df["scattering_coefficient_1/mm"].values

print(spectral_scattering_coefficient)


class ReceptorModel:
    def __init__(self):
        self.length = 5.4e-3  # thickness [m]
        self.n = 36  # the number of layers [-]
        self.dt = 10
        self.initial_temperature = 34
        self.t_core = 36.9
        self.t_db = 25
        self.t_r = 25
        self.q_total_irradiance = 0
        self.q_spectrum = np.zeros(len(wavelength))
        self.hc = (
            4  # convection heat transfer coefficient for human body in motion [W/m2]
        )
        self.hr = 5  # radiation heat transfer coefficient [W/m2]
        self._initialize_parameters()
        self.results = {}
        self.phases = []  # For storing simulation phases

    def _initialize_parameters(self):
        self.h = self.hc + self.hr  # heat transfer coefficient [W/m2K]
        dx = self.length / self.n  # length of each layer [m]
        self.node_coordinates = np.linspace(
            dx / 2, self.length - dx / 2, self.n
        )  # mass grid [m]

        self.capacity = 4.3e6 * dx  # heat capacity [J/m2/K]
        alpha = 0.25  # heat conductance of the human skin [W/mK]

        self.r_skin2core = dx / (
            2 * alpha
        )  # thermal resistance from skin to core [m2K/W]
        self.r_skin2skin = (
            dx / alpha
        )  # thermal resistance between skin mass points [m2K/W]
        self.r_skin2amb = (
            dx / (2 * alpha) + 1 / self.hc
        )  # thermal resistance from skin to ambient [m2K/W]

        self.a_sw = 0.70  # short wavelength absorption rate [-]
        self.a_lw = 0.97  # long wavelength absorption rate [-]

        self.sigma = 5.67e-8  # Stefan-Boltzmann constant [W/m2/K4]

    def add_phase(self, duration, t_db, t_r, q_irradiance):
        """
        Add a simulation phase with specific environmental conditions.

        Parameters:
        - duration (int): Duration of the phase in minutes.
        - t_db (float): Dry bulb temperature (°C).
        - t_r (float): Radiant temperature (°C).
        - q_irradiance (float): Total irradiance (W/m²).

        Raises:
        - ValueError: If any parameter is out of a reasonable range.
        """
        if duration <= 0:
            raise ValueError("Duration must be positive.")
        if not (0 <= t_db <= 50):
            raise ValueError("t_db must be within a reasonable range (0-50°C).")
        if not (0 <= t_r <= 50):
            raise ValueError("t_r must be within a reasonable range (0-50°C).")
        if q_irradiance < 0:
            raise ValueError("q_irradiance must be non-negative.")

        self.phases.append(
            {
                "duration": duration,
                "t_db": t_db,
                "t_r": t_r,
                "q_irradiance": q_irradiance,
            }
        )

    def update_environmental_conditions(self, phase):
        self.t_db = phase["t_db"]
        self.t_r = phase["t_r"]
        self.q_total_irradiance = phase["q_irradiance"]

    def calculate_radiation_distribution(
        self,
        q_spectral_irradiance,
        spectral_reflectance,
        spectral_absorption_coefficient,
        spectral_scattering_coefficient,
    ):
        """
        Calculate the distribution of radiation within the skin layers based on
        spectral irradiance and the optical properties of the skin.

        Parameters:
        - q_spectral_irradiance (float): The spectral irradiance (energy per unit area per unit time).
        - spectral_reflectance (float): The reflectance spectrum of the skin (fraction of reflected radiation).
        - spectral_absorption_coefficient (float): The absorption coefficient of the skin (per meter).
        - spectral_scattering_coefficient (float): The scattering coefficient of the skin (per meter).

        Returns:
        - numpy.ndarray: An array representing the distribution of radiation across the skin layers.
        """
        q_irradiance_nodes = []
        for x_cord in self.node_coordinates:
            tmp = (
                q_spectral_irradiance
                * (1 - spectral_reflectance)
                * (
                    np.exp(
                        -(
                            spectral_absorption_coefficient
                            + spectral_scattering_coefficient
                        )
                        * (x_cord - self.dx / 2)
                        * 1e3
                    )
                    - np.exp(
                        -(
                            spectral_absorption_coefficient
                            + spectral_scattering_coefficient
                        )
                        * (x_cord + self.dx / 2)
                        * 1e3
                    )
                )
            )
            tmp = tmp + tmp * self.dt / self.capacity
            q_irradiance_nodes.append(tmp.sum())
        return np.array(q_irradiance_nodes[::-1])

    def update_temperature_backward(self, T, q_irradiance_nodes):
        n = len(self.node_coordinates)
        A = np.zeros((n, n))  # Coefficient matrix
        b = np.zeros(n)  # Right-hand side vector

        q_irradiance_nodes = self.calculate_radiation_distribution(
            self,
            q_spectral_irradiance=self.q_total_irradiance * self.q_spectrum,
            spectral_reflectance=spectral_reflectance,
            spectral_absorption_coefficient=spectral_absorption_coefficient,
            spectral_scattering_coefficient=spectral_scattering_coefficient,
        )

        # Fill the coefficient matrix A and vector b based on backward difference scheme
        for i in range(1, n - 1):
            A[i, i - 1] = 1 / self.r_skin2skin
            A[i, i] = -1 / self.r_skin2skin * 2 - self.capacity / self.dt
            A[i, i + 1] = 1 / self.r_skin2skin
            b[i] = -T[i] * self.capacity / self.dt - q_irradiance_nodes[i]

        # Boundary conditions for the first and last layer
        A[0, 0] = 1 / self.r_skin2core + 1 / self.r_skin2skin + self.capacity / self.dt
        A[0, 1] = -1 / self.r_skin2skin
        b[0] = (self.t_core / self.r_skin2core + q_irradiance_nodes[0]) + T[
            0
        ] * self.capacity / self.dt

        A[-1, -2] = -1 / self.r_skin2skin
        A[-1, -1] = (
            1 / self.r_skin2amb
            + 1 / self.r_skin2skin
            + self.sigma * self.a_lw * (T[-1] + 273.15) ** 3 * 4
            + self.capacity / self.dt
        )
        b[-1] = (
            (self.t_db / self.r_skin2amb + q_irradiance_nodes[-1])
            + T[-1] * self.capacity / self.dt
            + self.sigma * self.a_lw * (self.t_r + 273.15) ** 4
        )

        # Solve the linear system
        T_new = np.linalg.solve(A, b)

        return T_new

    def simulate(self):
        if not self.phases:
            raise ValueError("At least one phase must be added before simulation.")

        T = (
            np.ones(self.n) * self.initial_temperature
        )  # Initial temperature distribution
        T_history = []

        for phase in self.phases:
            self.update_environmental_conditions(phase)
            time_steps = int(phase["duration"] * 60 / self.dt)

            for _ in range(time_steps):
                q_rd = np.ones(self.n) * self.q_total_irradiance
                T = self.update_temperature_backward(T, q_rd)
                T_history.append(T.copy())

        df = pd.DataFrame(T_history)
        df.columns = ["M" + str(i) for i in range(len(T))]

        # Additional Calculations
        df["M_warm"] = (df["M33"] + 5 * df["M32"]) / 6  # Warm receptor temperature
        df["dM_warm"] = df["M_warm"].diff()  # Derivative of warm receptor temperature
        df["Rt"] = (
            2 * (df["M_warm"]) + 56 * (df["dM_warm"]) / self.dt
        )  # Thermal response
        df["dRt"] = df["Rt"].diff()  # Derivative of thermal response
        df["I"] = (
            df["dRt"].rolling(int(20 / self.dt)).sum()
        )  # Integral of dRt over a window
        df["DTS"] = 5 * df["I"]  # Dermal Thermal Score

        self.results = df  # Store the dataframe in the class instance for later use

        return df


# Sample usage
# if __name__ == "__main__":
#     model = ReceptorModel()
#     model.add_phase(duration=10, t_db=20, t_r=25, q_irradiance=0)
#     model.add_phase(duration=10, t_db=30, t_r=27, q_irradiance=0)
#     simulation_results = model.simulate()
#
#     print(simulation_results)  # Print the temperature history
#     simulation_results.to_csv("test.csv")
