
import matplotlib.pyplot as plt
import pandas as pd
import os

# ----------File/Folder path configration----------
PROJECT_DIRECTORY = "C:\\Users\\monyo\\PycharmProjects\\wavelength" # (Please update as needed)

DATA_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "data")
RAW_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, "raw")
# PROCESSED_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, "processed")
# SUMMARY_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, "summary")

# Figure directory
figure_directory_name = "figures"
if not os.path.exists(figure_directory_name):
    os.makedirs(os.path.join(PROJECT_DIRECTORY, figure_directory_name), exist_ok=True)
FIGURE_PATH = os.path.join(PROJECT_DIRECTORY, figure_directory_name)

# --------------------

# plt.rcParams['font.family'] = 'Open Sans'
# sns.set()
# sns.set_palette(sns.color_palette("Set1"))
# # seaborn styles
# # https://seaborn.pydata.org/tutorial/aesthetics.html
# sns.set_style(
#     "ticks",{
#     "axes.grid": False,
#     "grid.color": "0.8",
#     'grid.linestyle': "dotted"})

#sns.set_style("ticks")

# # Graph setting
# plt.rcParams["font.family"] = "Arial"
# plt.rcParams['font.family'] ='sans-serif'#使用するフォント
plt.rcParams['xtick.direction'] = 'in'#x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in'#y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
# plt.rcParams["xtick.major.size"] = 4  #x軸主目盛り線の長さ
# plt.rcParams["ytick.major.size"] = 4  #y軸主目盛り線の長さ
# plt.rcParams["xtick.minor.size"] = 2  #x軸補助目盛り線の長さ
# plt.rcParams["ytick.minor.size"] = 2  #y軸補助目盛り線の長さ


# MAINPATH = "/content/drive/My Drive/00-研究活動/■B&E_MSM/"
# FIGPATH = "/content/drive/My Drive/00-研究活動/■B&E_MSM//1.Figure/査読回答用/"
# PDFPATH = "/content/drive/My Drive/00-研究活動/■B&E_MSM//1.Figure/査読回答用/pdf/"
# pd.options.display.precision = 2

# Constants
NOMOTO_EXP_PATH = "C:\\Users\\monyo\\PycharmProjects\\wavelength\\model_validation\\Nomoto's experiment_2021"
DATA_FILE_PATH = os.path.join(NOMOTO_EXP_PATH, "data\\filter_and_radiation_spectrum.xlsx")
FIGURE_SAVE_PATH = FIGURE_PATH  # You need to specify the actual save directory
INPUT_SPECTRUM_PATH = "C:\\Users\\monyo\\PycharmProjects\\wavelength\\model_validation\\Nomoto's experiment_2021\\input_summary.csv"