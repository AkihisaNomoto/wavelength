import os.path

import numpy as np
import pandas as pd
from pythermalcomfort.models import JOS3
from pythermalcomfort.jos3_functions.utilities import local_clo_typical_ensembles

import configration


def Nomoto2021(sex):
    # Mean Subject's anthropometric data
    if sex == "male":
        # Mean measured value
        model = JOS3(
            height=1.73,
            weight=64.9,
            fat=15,
            age=23,
            sex="male",
        )
    else:  # Female
        # Mean measured value
        model = JOS3(
            height=1.59,
            weight=49.7,
            fat=15,
            age=22,
            sex="female",
        )

    # Constant values
    model.posture = "sitting"
    model.par = 1.2  # presented in FAO/WHO/UNU

    # Phase 1
    # Sitting quietly for 60 min before irradiation
    model.tdb = 25.3  # Mean measured value
    model.tr = 25.0  # Mean measured value
    model.rh = 51  # Mean measured value
    model.v = 0.0  # Mean measured value
    # Wig, facemask, T-shirt, underwears, short pants, socks (No shoes)
    model.clo = {
        "head": 0.70,
        "neck": 0.65,
        "chest": 0.96,
        "back": 0.85,
        "pelvis": 1.30,
        "left_shoulder": 0.56,
        "left_arm": 0.03,
        "left_hand": 0.16,
        "right_shoulder": 0.56,
        "right_arm": 0.03,
        "right_hand": 0.16,
        "left_thigh": 0.39,
        "left_leg": 0.14,
        "left_foot": 0.38,
        "right_thigh": 0.39,
        "right_leg": 0.14,
        "right_foot": 0.38,
    }
    model.simulate(1000)

    df = pd.DataFrame(model.dict_results())
    df = df.tail(1).copy()  # Get only the last row
    df["experiment"] = "Nomoto_2021"

    if sex == "male":
        sex = "male"
    else:  # Female
        sex = "female"

    df["sex"] = sex

    return df.copy()


def Narita2001(sex):
    # Mean Subject's anthropometric data
    if sex == "male":
        model = JOS3(
            height=1.73,
            weight=57.6,
            fat=15,
            age=22,
            sex="male",
        )
    else:  # Female
        model = JOS3(
            height=1.62,
            weight=52.1,
            fat=15,
            age=22.7,
            sex="female",
        )

    model.posture = "sitting"
    model.PAR = 1.2

    # Phase 1
    # Sitting quietly for 60 min before irradiation
    model.tdb = 25.6  # Mean measured value
    model.tr = 26  # Mean measured value
    model.rh = 60  # Mean measured value
    model.v = 0.1  # Mean measured value
    # Y-shirt, underwears, long pants, socks (No shoes) #En. F
    model.clo = {
        "head": 0.50,
        "neck": 0,
        "chest": 0.86,
        "back": 0.86,
        "pelvis": 1.50,
        "left_shoulder": 0.82,
        "left_arm": 0.6,
        "left_hand": 0,
        "right_shoulder": 0.82,
        "right_arm": 0.60,
        "right_hand": 0,
        "left_thigh": 0.65,
        "left_leg": 0.66,
        "left_foot": 0.10,
        "right_thigh": 0.65,
        "right_leg": 0.66,
        "right_foot": 0.10,
    }
    model.simulate(1000)

    df = pd.DataFrame(model.dict_results())
    df = df.tail(1).copy()  # Get only the last row
    df["experiment"] = "Narita_2001"

    if sex == "male":
        sex = "male"
    else:  # Female
        sex = "female"

    df["sex"] = sex

    return df.copy()


def Matsui1986(sex):
    # Mean Subject's anthropometric data
    if sex == "male":
        model = JOS3(height=1.73, weight=57.6, fat=15, age=22, sex="male")
    else:  # Female
        model = JOS3(
            height=1.62,
            weight=52.1,
            fat=15,
            age=22.7,
            sex="female",
        )

    model.posture = "sitting"
    model.PAR = 1.2

    # Phase 1
    # Sitting quietly for 60 min before irradiation
    model.tdb = 19.5  # Mean measured value
    model.tr = 19.5  # Mean measured value
    model.rh = 60  # Mean measured value
    model.v = 0.1  # Mean measured value
    # Y-shirt, underwears, long pants, socks (No shoes) #En. F
    model.clo = {
        "head": 0.50,
        "neck": 0,
        "chest": 0.86,
        "back": 0.86,
        "pelvis": 1.50,
        "left_shoulder": 0.82,
        "left_arm": 0.6,
        "left_hand": 0,
        "right_shoulder": 0.82,
        "right_arm": 0.60,
        "right_hand": 0,
        "left_thigh": 0.65,
        "left_leg": 0.66,
        "left_foot": 0.10,
        "right_thigh": 0.65,
        "right_leg": 0.66,
        "right_foot": 0.10,
    }
    model.simulate(1000)

    df = pd.DataFrame(model.dict_results())
    df = df.tail(1).copy()  # Get only the last row
    df["experiment"] = "Matsui_1986"

    if sex == "male":
        sex = "male"
    else:  # Female
        sex = "female"

    df["sex"] = sex

    return df.copy()


dfs = []
dfs.append(Nomoto2021(sex="male"))
dfs.append(Nomoto2021(sex="female"))
dfs.append(Narita2001(sex="male"))
dfs.append(Narita2001(sex="female"))
dfs.append(Matsui1986(sex="male"))
dfs.append(Matsui1986(sex="female"))

sim = pd.concat(dfs)
sim = sim.reset_index(drop=True)

csv_path_name = "core_temperature_summary_simulated_by_JOS3.csv"
sim.to_csv(
    os.path.join(configration.DATA_DIRECTORY, csv_path_name)
)  # Write csv file (it takes some time)
print(sim["t_core_left_hand"])
