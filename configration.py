import os

# ----------File/Folder path configration----------
PROJECT_DIRECTORY = os.getcwd()
DATA_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "data")
FIGURE_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "figures")
NARITA_EXP_SPECTRUM_DATA_PATH = os.path.join(
    DATA_DIRECTORY, "Narita_1999_normalized_spectral_radiance.csv"
)
NOMOTO_EXP_SPECTRUM_DATA_PATH = os.path.join(
    DATA_DIRECTORY, "Nomoto_2021_spectral_irradiance_conditions.csv"
)
MATSUI_EXP_SPECTRUM_DATA_PATH = os.path.join(
    DATA_DIRECTORY, "Matsui_1986_spectral_irradiance_conditions.csv"
)
