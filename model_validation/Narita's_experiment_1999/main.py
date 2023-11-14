import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import configration as config
from pythermalcomfort.models import JOS3

from model import ReceptorModel

# Constants
DATA_FILE_PATH = "C:\\Users\\monyo\\PycharmProjects\\wavelength\\model_validation\\Narita's_experiment_1999\\normalized_spectral_radiance.csv"

# Define radiation intensity (each condition is the same value)
radiation_intensity = 1220 # [W/m2]

# Read the data
df = pd.read_csv(DATA_FILE_PATH)
df.columns = ["wavelength", "Visible (0.30–0.84 µm)", "Near-infrared (0.80 – 1.35 µm)", "Mid-infrared (1.70 – 2.30 µm)"]

# -------------------------------------------------------------------------------
# JOS-3 simulation to get core temperature
# -------------------------------------------------------------------------------

# def simulate_experiment_by_JOS3(person, conslib=None):
#     """
#     Runs the JOS3 simulation for both male and female conditions and combines the results.
#
#     Returns:
#     - DataFrame: The simulation results for both conditions.
#     """
#     # Mean Subject's anthropometric data
#     if person == "male":
#         model = JOS3(
#             height=1.71,
#             weight=63.2,
#             fat=15,
#             age=23,
#             sex="male",
#             bmr_equation="japanese",
#         )
#     elif person=="female":  # Female
#         model = JOS3(
#             height=1.59,
#             weight=49.7,
#             fat=15,
#             age=21,
#             # sex="female",
#             bmr_equation="japanese",
#         )
#     else:
#         print("Please select either 'male' or 'female'.")
#
#     # Set experimental conditions
#     model.posture = "sitting"
#     model.par = 1.2
#     model.tdb = 24.7
#     model.tr = 25.5
#     model.rh = 67
#     model.v = 0.06
#     model.clo = np.array(
#         [
#             0.6,
#             0,
#             0.86,
#             0.86,
#             1.50,
#             0.82,
#             0.60,
#             0,
#             0.82,
#             0.60,
#             0,
#             0.65,
#             0.66,
#             0.1,
#             0.65,
#             0.66,
#             0.1,
#         ]
#     )  # Y-shirt, underwears, long pants, socks (No shoes) # En. F
#
#     # Simulate
#     model.simulate(times=100, dtime=600)
#
#     df = pd.DataFrame(model.dict_results().copy())
#     df = df.iloc[[-1]].copy()  # Get last step results
#
#     if person == "male":
#         cond = "male"
#     else:  # Female
#         cond = "female"
#
#     df["Condition"] = cond
#
#     return df
#
#
# dfs = []
# dfs.append(simulate_experiment_by_JOS3(person="male"))
# dfs.append(simulate_experiment_by_JOS3(person="female"))
#
# sim = pd.concat(dfs)
# # sim = sim.reset_index(drop=True)
# csv_path = "JOS-3_simulation_results_Narita1994.csv"
# sim.to_csv(csv_path)
#
# t_core_hand = sim["t_core_left_hand"].mean()
# print(f"Hand core temperature: {t_core_hand}")

# Thremoreceptor simulation

result = {}
