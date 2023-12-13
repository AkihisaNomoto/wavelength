import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import configration as config
from sklearn import linear_model
from sklearn.metrics import r2_score

# Set global matplotlib parameters for font
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.get_cmap("Set1").colors)

df = pd.read_csv(os.path.join(config.DATA_DIRECTORY, "psi_vs_sensation_vote.csv"))
df.columns = ["Exp", "ΔPSI/PSI","ΔTSV","ΔTSV_ERR"]

#The areas equals to radiation energy.
x = df["ΔPSI/PSI"].values
y = df["ΔTSV"].values
y_err = df["ΔTSV_ERR"].values

# Narita
x_narita = df.loc[0:2,"ΔPSI/PSI"].values
y_narita = df.loc[0:2,"ΔTSV"].values
y_err_narita = df.loc[0:2,"ΔTSV_ERR"].values

#Matsui
x_matsui = df.loc[3:5,"ΔPSI/PSI"].values
y_matsui = df.loc[3:5,"ΔTSV"].values
y_err_matsui = df.loc[3:5,"ΔTSV_ERR"].values

#Nomoto
x_nomoto = df.loc[6:8,"ΔPSI/PSI"].values
y_nomoto = df.loc[6:8,"ΔTSV"].values
y_err_nomoto = df.loc[6:8,"ΔTSV_ERR"].values

plt.figure(figsize=(6,3.5))
#plt.scatter(x, y, color="black", facecolor="white")
plt.errorbar(x_narita, y_narita, y_err_narita,capsize=0, fmt='o', markersize=8, ecolor='lightgrey', markeredgecolor = "black", color='w', label="Narita et al. (2001)")
plt.errorbar(x_matsui, y_matsui, y_err_matsui,capsize=0, fmt='s', markersize=8, ecolor='lightgrey', markeredgecolor = "black", color='w', label="Matsui et al. (1986)")
plt.errorbar(x_nomoto, y_nomoto, y_err_nomoto,capsize=0, fmt='^', markersize=8, ecolor='lightgrey', markeredgecolor = "black", color='w', label="Nomoto et al. (This study)")

plt.xlim(0,0.6)
plt.ylim(-3,3)
y = [-3, -2, -1, 0, 1, 2, 3]
plt.yticks(y, ["very hot  -3", "hot  -2", "slightly hot  -1", "neutral  0", "slightly hot  +1", "hot  +2", "very hot  +3"])


x = df[["ΔPSI/PSI"]]
y = df[["ΔTSV"]]
model = linear_model.LinearRegression(fit_intercept=False)
model.fit(x,y)
a = round(model.coef_[0][0], 2)
print(a)
y_predict = model.predict(x)
#r2 = model.score(y_predict, y)
r2 = round(r2_score(y, y_predict),2)
# plt.plot(x, y_predict, color = 'black', linestyle = 'solid', label = "y = %.3f" % model.coef_[0] +"x"+" (R$\mathregular{^2}$ = 0.52)", alpha=0.5)
plt.plot(x, y_predict, color = 'black', linestyle = 'solid', label = f"y = {a}x (R$\mathregular{{^2}}$ = {r2})", alpha=0.5)
plt.axhline(0, 0, 1, linestyle = "dotted", color="lightgrey")
plt.tick_params(pad=6)

plt.xlabel("ΔPSI ratio [-]")
plt.ylabel("Relative thermal sensation [-]")
plt.tight_layout() #topを96%に縮小
#plt.legend(bbox_to_anchor=(0.5, 1.2), ncol=3, loc='upper center',frameon=False)
plt.legend(bbox_to_anchor=(0.98, 0.04),loc='lower right')
plt.savefig(os.path.join(config.FIGURE_DIRECTORY, "psi_vs_sensation_votes.svg"))
plt.show()

print('モデル関数の回帰変数 w1: %.3f' % model.coef_)
print('モデル関数の切片 w2: %.3f' %model.intercept_)
print('y= %.3fx + %.3f' % (model.coef_, model.intercept_))
print('決定係数 R^2： ', model.score(x, y))

#yの標本分散
sy2 = y.var()
#線形回帰式との誤差を計算
d = y - y_predict
#誤差の2乗平均を計算
syx2 = np.mean(d**2)
#sr^2を計算
sr2 = sy2 - syx2
#決定係数計算
r2 = sr2/sy2

print(r2) #0.9891203611402715

# import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score
# import configration as config
#
# # Set global matplotlib parameters
# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.get_cmap("Set1").colors)
#
# # Load data
# df = pd.read_csv(os.path.join(config.DATA_DIRECTORY, "psi_vs_sensation_vote.csv"))
# df.columns = ["Exp", "ΔPSI/PSI", "ΔTSV", "ΔTSV_ERR"]
#
# # Data preparation
# x = df["ΔPSI/PSI"].values.reshape(-1, 1)
# y = df["ΔTSV"].values
#
# # Linear regression
# model = LinearRegression(fit_intercept=True)
# model.fit(x, y)
# y_predict = model.predict(x)
# r2 = r2_score(y, y_predict)
#
# # Plotting
# plt.figure(figsize=(7.5, 4))
# # Plot error bars for different studies
# for study in ["Narita", "Matsui", "Nomoto"]:
#     indices = df["Exp"].str.contains(study)
#     plt.errorbar(df[indices]["ΔPSI/PSI"], df[indices]["ΔTSV"], df[indices]["ΔTSV_ERR"],
#                  capsize=0, fmt='o', markersize=8, ecolor='lightgrey',
#                  markeredgecolor="black", color='w', label=f"{study} et al.")
#
# plt.plot(x, y_predict, color='black', linestyle='solid',
#          label=f"y = {model.coef_[0]:.3f}x + {model.intercept_:.3f} (R$^{{2}}$ = {r2:.2f})", alpha=0.5)
#
# plt.axhline(0, 0, 1, linestyle="dotted", color="lightgrey")
# plt.xlim(0, 0.6)
# plt.ylim(-3, 3)
# plt.yticks(range(-3, 4), ["very hot -3", "hot -2", "slightly hot -1", "neutral 0", "slightly hot +1", "hot +2", "very hot +3"])
# plt.xlabel("ΔPSI ratio [-]")
# plt.ylabel("Relative thermal sensation [-]")
# plt.tight_layout()
# plt.legend(loc='lower right')
# plt.savefig(os.path.join(config.FIGURE_DIRECTORY, "psi_vs_sensation_votes.svg"))
# plt.show()
#
# # Print model results
# print(f'モデル関数の回帰変数 w1: {model.coef_[0]:.3f}')
# print(f'モデル関数の切片 w2: {model.intercept_:.3f}')
# print(f'y= {model.coef_[0]:.3f}x + {model.intercept_:.3f}')
# print(f'決定係数 R^2： {r2:.4f}')
