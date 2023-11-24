import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import configration as config

# Set global matplotlib parameters for font
plt.rcParams['font.family'] = 'Arial'

# Constants
DATA_FILE_PATH = os.path.join(config.DATA_DIRECTORY, "Nomoto_2021_experimental_data.xlsx")

# Read the data
df = pd.read_excel(DATA_FILE_PATH, sheet_name="箱ひげ図２")


df.columns = ["sex", "cond",
              "before_whole_TSV", "before_whole_TCV", "before_left_TSV", "before_right_TSV", "before_left_TCV", "before_right_TCV",
              "after_left_TSV", "after_right_TSV", "after_left_TCV","after_right_TCV", "after_comparison_TSV","after_comparison_TCV",  "after5min_comparison_TSV","after5min_comparison_TCV"]

print(df)

fig, axes = plt.subplots(3, 2, sharex=True, figsize=(12,6))
# axes[0]

whole = df.copy()
male = df.loc[df["sex"]=="男性"].copy()
female = df.loc[df["sex"]=="女性"].copy()

TSV = {}
TCV = {}
mean = {}
for i, cond in enumerate(["AとB","BとC","AとC"]):
  #温冷感
  TSV_male = male.loc[male["cond"]==cond]["after_comparison_TSV"].values.tolist() #リストに変換
  TSV_female = female.loc[female["cond"]==cond]["after_comparison_TSV"].values.tolist() #リストに変換
  TSV_whole = whole.loc[whole["cond"]==cond]["after_comparison_TSV"].values.tolist() #リストに変換
  #快適感
  TCV_male = male.loc[male["cond"]==cond]["after_comparison_TCV"].values.tolist() #リストに変換
  TCV_female = female.loc[female["cond"]==cond]["after_comparison_TCV"].values.tolist() #リストに変換
  TCV_whole = whole.loc[whole["cond"]==cond]["after_comparison_TCV"].values.tolist() #リストに変換
  #組み合わせる
  TSV[cond] = (TSV_whole, TSV_female, TSV_male)
  TCV[cond] = (TCV_whole, TCV_female, TCV_male)
  mean = sum(TSV_whole)/len(TSV_whole)
  print(mean)
  #補助線
  for j in [-3,-2,-1,0,1,2,3]:
    axes[i,0].axvline(j, 0, 2, linestyle = "dotted", color="lightgray")
    axes[i,1].axvline(j, 0, 2, linestyle = "dotted", color="lightgray")
  #中心線を作図
  axes[i,0].axvline(0, 0, 2, linestyle = "solid", color="black")
  axes[i,1].axvline(0, 0, 2, linestyle = "solid", color="black")
  #箱ひげ図の作成
  colorlists = ["blue","red","black"] # 色指定
  #温冷感
  bp1 = axes[i,0].boxplot(TSV[cond],vert=False,  # 横向きにする
                  patch_artist=True,  # 細かい設定をできるようにする
                  showmeans=False, #平均値を表示
                  meanprops=dict(marker="x", markersize=4, markeredgecolor="black"),  # 平均値の設定
                  widths=0.5,  # boxの幅の設定
                  boxprops=dict(facecolor= "white",  # boxの塗りつぶし色の設定
                                color='black'),  # boxの枠線の設定
                  medianprops=dict(linewidth=1.5),  # 中央値の線の設定
                  whiskerprops=dict(color='black'),  # ヒゲの線の設定
                  capprops=dict(color='black'),  # ヒゲの先端の線の設定
                  flierprops=dict(markeredgecolor='black',markersize=5)  # 外れ値の設定
                  )
  #快適感
  bp2 = axes[i,1].boxplot(TCV[cond],vert=False,  # 横向きにする
                patch_artist=True,  # 細かい設定をできるようにする
                showmeans=False, #平均値を表示
                meanprops=dict(marker="x", markersize=4, markeredgecolor="black"),  # 平均値の設定
                widths=0.5,  # boxの幅の設定
                boxprops=dict(facecolor= "white",  # boxの塗りつぶし色の設定
                              color='black'),  # boxの枠線の設定
                medianprops=dict(linewidth=1.5),  # 中央値の線の設定
                whiskerprops=dict(color='black'),  # ヒゲの線の設定
                capprops=dict(color='black'),  # ヒゲの先端の線の設定
                flierprops=dict(markeredgecolor='black',markersize=5)  # 外れ値の設定
                )

  # 色の設定
  # boxの色のリスト
  colors=["black", "red", "blue"]
  colors2=["black", "black", "red", "red", "blue", "blue"]
  # boxの色の設定
  for b, c in zip(bp1['boxes'], colors):
      b.set(color=c)  # boxの外枠の色
      b.set_facecolor("white") # boxの色
      b.set_edgecolor(c)
  # 中央値の線の設定
  for b, c in zip(bp1['medians'], colors):
      b.set(color=c)
  # 平均値値の線の設定
  for b, c in zip(bp1['means'], colors):
      b.set(marker="x", markersize=4, markeredgecolor=c)
  # ヒゲの線の設定
  for b, c in zip(bp1['whiskers'], colors2):
      b.set(color=c)
  # ヒゲの先端の線の設定
  for b, c in zip(bp1['caps'], colors2):
      b.set(color=c)
  # 外れ値の設定
  for b, c in zip(bp1['fliers'], colors):
      b.set(markeredgecolor=c)

  # boxの色の設定
  for b, c in zip(bp2['boxes'], colors):
      b.set(color=c)  # boxの外枠の色
      b.set_facecolor("white") # boxの色
      b.set_edgecolor(c)
  # 中央値の線の設定
  for b, c in zip(bp2['medians'], colors):
      b.set(color=c)
  # 平均値値の線の設定
  for b, c in zip(bp2['means'], colors):
      b.set(marker="x", markersize=4, markeredgecolor=c)
  # ヒゲの線の設定
  for b, c in zip(bp2['whiskers'], colors2):
      b.set(color=c)
  # ヒゲの先端の線の設定
  for b, c in zip(bp2['caps'], colors2):
      b.set(color=c)
  # 外れ値の設定
  for b, c in zip(bp2['fliers'], colors):
      b.set(markeredgecolor=c)

# Add subplot labels ('a)' and 'b)')
subplot_labels = ['a', 'b']
survey_questions = [
    "Please rate which radiation you feel hotter.",
    "Please rate which radiation you feel comfortable."
              ]
label_height = 4.8
axes[0,0].text(-3.5, label_height, subplot_labels[0], fontsize=14, fontweight='bold', va='center', ha='right')
axes[0,1].text(-3.5, label_height, subplot_labels[1], fontsize=14, fontweight='bold', va='center', ha='right')
axes[0,0].text(-3.5, label_height, survey_questions[0], fontsize=12, fontstyle='italic', va='center', ha='left')
axes[0,1].text(-3.5, label_height, survey_questions[0], fontsize=12, fontstyle='italic', va='center', ha='left')

for i, names in enumerate(["Male (N=10)", "Female (N=10)", "All subjects (N=20)",]):
  #axes[i,0].set_yticklabels(["All subjects", "Female", "Male"])
  axes[i,0].set_xticks([-3,-2,-1,0,1,2,3])
  axes[2,0].set_xticklabels(["-3", "-2", "-1", "0", "+1", "+2", "+3"])
  labal_height = 5
  #凡例を記述
  axes[0,0].text(2.4*i+1, labal_height, names,verticalalignment="center",fontsize=12)
  colors=["blue", "red","black"]
  axes[0,0].text(2.4*i+0.5, labal_height+0.1, "□" ,color=colors[i],verticalalignment="center",fontsize=20, fontweight="bold")
  axes[i,0].tick_params(left=False,labelleft=False)
  axes[i,1].tick_params(left=False,labelleft=False)

  # テキスト用の四角
  boxdic = {
    "facecolor" : "white",
    "edgecolor" : "black",
    "linewidth" : 1
    }
  # title = ["A and B", "B and C", "A and C"]
  # axes[i,0].text(-2.8, 2.5, title[i], size=10, bbox=boxdic) # テキスト
  title = ["A", "B", "A"]
  axes[i,0].text(-3.6, 1.9, title[i], fontsize=12) # テキスト
  axes[i,1].text(-3.6, 1.9, title[i], fontsize=12) # テキスト
  title = ["B", "C", "C"]
  axes[i,0].text(3.4, 1.9, title[i], fontsize=12) # テキスト
  axes[i,1].text(3.4, 1.9, title[i], fontsize=12) # テキスト

#テキスト入力
for i, names in enumerate(["very hot", "hot", "slightly hot", "neutral", "slightly hot", "hot", "very hot"]):
  axes[2,0].text(i-3, -0.4, names ,verticalalignment="center",horizontalalignment="center",fontsize=10)
for i, names in enumerate(["very comf.", "comf.", "slightly comf.", "neutral", "slightly comf.", "comf.", "very comf."]):
  axes[2,1].text(i-3, -0.4, names ,verticalalignment="center",horizontalalignment="center",fontsize=10)

#テキスト入力
# axes[0,0].text(0, 4, " → radiation of longer wavelength",horizontalalignment="left", fontsize=10)
# axes[0,0].text(0, 4, "radiation of shorter wavelength ← ",horizontalalignment="right", fontsize=10)
# axes[0,1].text(0, 4, " → radiation of longer wavelength",horizontalalignment="left", fontsize=10)
# axes[0,1].text(0, 4, "radiation of shorter wavelength ← ",horizontalalignment="right", fontsize=10)

for i in [0, 1]:
    axes[0,i].set_title("A vs B", fontsize=12)
    axes[1,i].set_title("B vs C", fontsize=12)
    axes[2,i].set_title("A vs C", fontsize=12)

# axes[0,1].set_xlabel("title1", fontsize=12)
# axes[0,2].set_xlabel("title3", fontsize=12)

axes[2,0].set_xlabel("Relative thermal sensation [-]", labelpad=18,fontsize=12)
axes[2,1].set_xlabel("Relative thermal comfort [-]", labelpad=18,fontsize=12)
plt.subplots_adjust(hspace=1)
fig.tight_layout()
plt.subplots_adjust(wspace=0.15, hspace=0.3)


#handles, labels0 = axes[0].get_legend_handles_labels() # axes[0]のhandleとlabelを取得
fig.savefig(os.path.join(config.FIGURE_DIRECTORY, "Nomoto_2021_experimental_results_.svg"))
plt.show()



# ##
# #　5分後
# ##
# fig, axes = plt.subplots(3, 2, sharex=True, figsize=(12,4.5))
# # axes[0]
#
# whole = df.copy()
# male = df.loc[df["sex"]=="男性"].copy()
# female = df.loc[df["sex"]=="女性"].copy()
#
# TSV = {}
# TCV = {}
# mean = {}
# for i, cond in enumerate(["AとB","BとC","AとC"]):
#   #温冷感
#   TSV_male = male.loc[male["cond"]==cond]["after5min_comparison_TSV"].values.tolist() #リストに変換
#   TSV_female = female.loc[female["cond"]==cond]["after5min_comparison_TSV"].values.tolist() #リストに変換
#   TSV_whole = whole.loc[whole["cond"]==cond]["after5min_comparison_TSV"].values.tolist() #リストに変換
#   #快適感
#   TCV_male = male.loc[male["cond"]==cond]["after5min_comparison_TCV"].values.tolist() #リストに変換
#   TCV_female = female.loc[female["cond"]==cond]["after5min_comparison_TCV"].values.tolist() #リストに変換
#   TCV_whole = whole.loc[whole["cond"]==cond]["after5min_comparison_TCV"].values.tolist() #リストに変換
#   #組み合わせる
#   TSV[cond] = (TSV_whole, TSV_female, TSV_male)
#   TCV[cond] = (TCV_whole, TCV_female, TCV_male)
#   mean = sum(TSV_whole)/len(TSV_whole)
#   print(mean)
#   #補助線
#   for j in [-3,-2,-1,0,1,2,3]:
#     axes[i,0].axvline(j, 0, 2, linestyle = "dotted", color="lightgray")
#     axes[i,1].axvline(j, 0, 2, linestyle = "dotted", color="lightgray")
#   #中心線を作図
#   axes[i,0].axvline(0, 0, 2, linestyle = "solid", color="black")
#   axes[i,1].axvline(0, 0, 2, linestyle = "solid", color="black")
#   #箱ひげ図の作成
#   colorlists = ["blue","red","black"] # 色指定
#   #温冷感
#   bp1 = axes[i,0].boxplot(TSV[cond],vert=False,  # 横向きにする
#                   patch_artist=True,  # 細かい設定をできるようにする
#                   showmeans=False, #平均値を表示
#                   meanprops=dict(marker="x", markersize=4, markeredgecolor="black"),  # 平均値の設定
#                   widths=0.5,  # boxの幅の設定
#                   boxprops=dict(facecolor= "white",  # boxの塗りつぶし色の設定
#                                 color='black'),  # boxの枠線の設定
#                   medianprops=dict(linewidth=1.5),  # 中央値の線の設定
#                   whiskerprops=dict(color='black'),  # ヒゲの線の設定
#                   capprops=dict(color='black'),  # ヒゲの先端の線の設定
#                   flierprops=dict(markeredgecolor='black',markersize=5)  # 外れ値の設定
#                   )
#   #快適感
#   bp2 = axes[i,1].boxplot(TCV[cond],vert=False,  # 横向きにする
#                 patch_artist=True,  # 細かい設定をできるようにする
#                 showmeans=False, #平均値を表示
#                 meanprops=dict(marker="x", markersize=4, markeredgecolor="black"),  # 平均値の設定
#                 widths=0.5,  # boxの幅の設定
#                 boxprops=dict(facecolor= "white",  # boxの塗りつぶし色の設定
#                               color='black'),  # boxの枠線の設定
#                 medianprops=dict(linewidth=1.5),  # 中央値の線の設定
#                 whiskerprops=dict(color='black'),  # ヒゲの線の設定
#                 capprops=dict(color='black'),  # ヒゲの先端の線の設定
#                 flierprops=dict(markeredgecolor='black',markersize=5)  # 外れ値の設定
#                 )
#
#   # 色の設定
#   # boxの色のリスト
#   colors=["black", "red", "blue"]
#   colors2=["black", "black", "red", "red", "blue", "blue"]
#   # boxの色の設定
#   for b, c in zip(bp1['boxes'], colors):
#       b.set(color=c)  # boxの外枠の色
#       b.set_facecolor("white") # boxの色
#       b.set_edgecolor(c)
#   # 中央値の線の設定
#   for b, c in zip(bp1['medians'], colors):
#       b.set(color=c)
#   # 平均値値の線の設定
#   for b, c in zip(bp1['means'], colors):
#       b.set(marker="x", markersize=4, markeredgecolor=c)
#   # ヒゲの線の設定
#   for b, c in zip(bp1['whiskers'], colors2):
#       b.set(color=c)
#   # ヒゲの先端の線の設定
#   for b, c in zip(bp1['caps'], colors2):
#       b.set(color=c)
#   # 外れ値の設定
#   for b, c in zip(bp1['fliers'], colors):
#       b.set(markeredgecolor=c)
#
#   # boxの色の設定
#   for b, c in zip(bp2['boxes'], colors):
#       b.set(color=c)  # boxの外枠の色
#       b.set_facecolor("white") # boxの色
#       b.set_edgecolor(c)
#   # 中央値の線の設定
#   for b, c in zip(bp2['medians'], colors):
#       b.set(color=c)
#   # 平均値値の線の設定
#   for b, c in zip(bp2['means'], colors):
#       b.set(marker="x", markersize=4, markeredgecolor=c)
#   # ヒゲの線の設定
#   for b, c in zip(bp2['whiskers'], colors2):
#       b.set(color=c)
#   # ヒゲの先端の線の設定
#   for b, c in zip(bp2['caps'], colors2):
#       b.set(color=c)
#   # 外れ値の設定
#   for b, c in zip(bp2['fliers'], colors):
#       b.set(markeredgecolor=c)
#
# for i, names in enumerate(["Male (N=10)", "Female (N=10)", "All subjects (N=20)",]):
#   #axes[i,0].set_yticklabels(["All subjects", "Female", "Male"])
#   axes[i,0].set_xticks([-3,-2,-1,0,1,2,3])
#   axes[2,0].set_xticklabels(["-3", "-2", "-1", "0", "+1", "+2", "+3"])
#   #凡例を記述
#   axes[0,0].text(2.4*i+1, 5.3, names,verticalalignment="center",fontsize=10)
#   colors=["blue", "red","black"]
#   axes[0,0].text(2.4*i+0.5, 5.4, "□" ,color=colors[i],verticalalignment="center",fontsize=10)
#   axes[i,0].tick_params(left=False,labelleft=False)
#   axes[i,1].tick_params(left=False,labelleft=False)
#
#   # テキスト用の四角
#   boxdic = {
#     "facecolor" : "white",
#     "edgecolor" : "black",
#     "linewidth" : 1
#     }
#   # title = ["A and B", "B and C", "A and C"]
#   # axes[i,0].text(-2.8, 2.5, title[i], size=10, bbox=boxdic) # テキスト
#   title = ["A", "B", "A"]
#   axes[i,0].text(-3.7, 1.9, title[i], fontsize=10) # テキスト
#   axes[i,1].text(-3.7, 1.9, title[i], fontsize=10) # テキスト
#   title = ["B", "C", "C"]
#   axes[i,0].text(3.5, 1.9, title[i], fontsize=10) # テキスト
#   axes[i,1].text(3.5, 1.9, title[i], fontsize=10) # テキスト
#
# #テキスト入力
# for i, names in enumerate(["very hot", "hot", "slightly hot", "neutral", "slightly hot", "hot", "very hot"]):
#   axes[2,0].text(i-3, -0.7, names ,verticalalignment="center",horizontalalignment="center",fontsize=9)
# for i, names in enumerate(["very comf.", "comf.", "slightly comf.", "neutral", "slightly comf.", "comf.", "very comf."]):
#   axes[2,1].text(i-3, -0.7, names ,verticalalignment="center",horizontalalignment="center",fontsize=9)
#
# #テキスト入力
# axes[0,0].text(0, 4, " → radiation of longer wavelength",horizontalalignment="left", fontsize=10)
# axes[0,0].text(0, 4, "radiation of shorter wavelength ← ",horizontalalignment="right", fontsize=10)
# axes[0,1].text(0, 4, " → radiation of longer wavelength",horizontalalignment="left", fontsize=10)
# axes[0,1].text(0, 4, "radiation of shorter wavelength ← ",horizontalalignment="right", fontsize=10)
#
# axes[2,0].set_xlabel("Relative thermal sensation [-]", labelpad=18,fontsize=10)
# axes[2,1].set_xlabel("Relative thermal comfort [-]", labelpad=18,fontsize=10)
# plt.subplots_adjust(hspace=0)
# fig.tight_layout()
# plt.subplots_adjust(wspace=0.15, hspace=0)
# #handles, labels0 = axes[0].get_legend_handles_labels() # axes[0]のhandleとlabelを取得
# # fig.savefig(FIGPATH + "B&E_MSM_Nomoto2021_Comparison_5min【博士論文用の図】.svg")
# plt.show()
