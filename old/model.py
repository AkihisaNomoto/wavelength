import numpy as np
import pandas as pd

# Global parameters
t_final = 20  # Final time [s]
dt = 0.05  # Time step [s]
L = 5.4e-3  # Thickness [m]
n = 36  # Number of layers
dx = L / n  # Length of each layer [m]
capacity = 4.3e6 * dx  # Heat capacity [J/m2/K]
alpha = 0.25  # Thermal conductance of the human skin [W/mK]
σ = 5.67e-8  # Stefan-Boltzmann constant [W/m2/K^4]

# Initial and environmental temperatures
T0 = 34  # Initial temperature [°C]
T_cr = 37  # Core temperature [°C]
T_a = 24.7  # Ambient air temperature [°C]
T_r = 25.5  # Mean radiant temperature [°C]

# Heat transfer coefficients calculation
hc = 6.4  # Convection heat transfer coefficient for human body in motion [W/m2]
hr = 5.1  # Radiation heat transfer coefficient [W/m2]
h = hc + hr  # Overall heat transfer coefficient [W/m2K]

# Thermal resistance calculations
r_skin2core = dx / (2 * alpha)  # Thermal resistance from skin to core [m2K/W]
r_skin2skin = dx / alpha  # Thermal resistance between skin mass points [m2K/W]
r_skin2amb = dx / (2 * alpha) + 1 / hc  # Thermal resistance from skin to ambient [m2K/W]

# Absorptance and reflectance
a_sw = 0.70  # Short-wave absorptance [-]
a_lw = 0.97  # Long-wave absorptance [-]


# Retrieve reflectance, absorption, and scattering coefficients from df3 (depends on df3 structure)
# ref, ab, scat = df3['ref'].values, df3['ab'].values, df3['scat'].values

# Function to get the temperature list
def get_Tlist(T_a, T_r, simulation_time, T, q_ir, radiance_properties):
    mass_cordinations = np.linspace(dx / 2, L - dx / 2, n)
    t = np.arange(0, simulation_time, dt)

    q_rd = radiance_energy_calculation(q_ir, radiance_properties, mass_cordinations)

    T_history = [T.copy()]

    # Heat balance equations
    for current_time in t[1:]:
        q_in = calculate_heat_flux(T, q_rd)

        # Update temperature
        T += q_in * dt / capacity
        T_history.append(T.copy())

    return T_history


# Function to calculate radiance energy
def radiance_energy_calculation(q_ir, radiance_properties, mass_cordinations):
    ref, ab, scat = radiance_properties
    q_rd = []
    for xcord in mass_cordinations:
        # Calculate radiance energy at each mass point
        energy = q_ir * (1 - ref) * (np.exp(-(ab + scat) * (xcord - dx / 2) * 1e3) -
                                     np.exp(-(ab + scat) * (xcord + dx / 2) * 1e3))
        q_rd.append(energy.sum())  # Sum over the spectrum
    return np.array(q_rd[::-1])  # Reverse array as the core side coordinate is 0


# Function to calculate heat flux
def calculate_heat_flux(T, q_rd):
    q_in = np.zeros(n)
    q_in[1:-1] = (T[:-2] - T[1:-1]) / r_skin2skin + (T[2:] - T[1:-1]) / r_skin2skin + q_rd[1:-1]
    q_in[0] = (T[1] - T[0]) / r_skin2skin + (T_cr - T[0]) / r_skin2core + q_rd[0]
    q_in[-1] = (T[-2] - T[-1]) / r_skin2skin + (T_a - T[-1]) / r_skin2amb + \
               σ * a_lw * (T_r + 273.15) ** 4 - σ * a_lw * (T[-1] + 273.15) ** 4 + q_rd[-1]
    return q_in

