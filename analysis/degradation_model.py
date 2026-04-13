"""
F1 Tyre Degradation Analysis(using Linear Regression)
2023 Italian GP (Monza) — VER vs SAI vs NOR
Linear regression model measuring tyre deg rate per lap.
"""

import fastf1
import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("f1_cache",exist_ok=True)
fastf1.Cache.enable_cache("f1_cache")

session = fastf1.get_session(2023,"Monza","R")
session.load()

laps = session.laps
#Filter Drivers
verstappen_laps = laps.pick_drivers("VER").copy()
sainz_laps = laps.pick_drivers("SAI").copy()
norris_laps = laps.pick_drivers("NOR").copy()
#LapTime
verstappen_laps["LapTimeSeconds"] = verstappen_laps["LapTime"].dt.total_seconds()
sainz_laps["LapTimeSeconds"] = sainz_laps["LapTime"].dt.total_seconds()
norris_laps["LapTimeSeconds"] = norris_laps["LapTime"].dt.total_seconds()

#Hard Stint
ver_stint = verstappen_laps[
    (verstappen_laps["Compound"] == "HARD") &
    (verstappen_laps["LapTimeSeconds"] < 105) &
    (verstappen_laps["LapNumber"] <= 51)
].copy()

sai_stint = sainz_laps[
    (sainz_laps["Compound"] == "HARD" ) &
    (sainz_laps["LapTimeSeconds"] < 105) &
    (sainz_laps["LapNumber"] <=51)
].copy()

nor_stint = norris_laps[
    (norris_laps["Compound"] == "HARD" ) &
    (norris_laps["LapTimeSeconds"] < 105) &
    (norris_laps["LapNumber"] < 51)
].copy()

#Array
x_ver = ver_stint["LapNumber"].values
y_ver = ver_stint["LapTimeSeconds"].values
x_sai = sai_stint["LapNumber"].values
y_sai = sai_stint["LapTimeSeconds"].values
x_nor = nor_stint["LapNumber"].values
y_nor = nor_stint["LapTimeSeconds"].values
#Calculate Regression
slope_ver,intercept_ver =np.polyfit(x_ver,y_ver,1)
slope_sai,intercept_sai =np.polyfit(x_sai,y_sai,1)
slope_nor,intercept_nor =np.polyfit(x_nor,y_nor,1)

regression_ver = slope_ver * x_ver + intercept_ver
regression_sai = slope_sai * x_sai +intercept_sai
regression_nor = slope_nor * x_nor + intercept_nor

#Plot
fig , ax = plt.subplots(figsize=(12,6))

ax.scatter(x_ver,y_ver,color="green",zorder = 5,s=40,label="Verstappen laps")
ax.scatter(x_sai,y_sai,linewidth=2,color="pink",zorder = 5,s=40,label="Sainz laps")
ax.scatter(x_nor,y_nor,linewidth=2,color="purple",zorder = 5, s=40,label="Norris laps")

ax.plot(x_ver,regression_ver,color="red",zorder = 5,linewidth = 2, linestyle ="--",label=f"VER deg:{round(slope_ver,4)}s/lap")
ax.plot(x_sai,regression_sai,color = "cyan",zorder = 5,linewidth = 2,linestyle ="--",label=f"SAI deg:{round(slope_sai,4)}s/lap")
ax.plot(x_nor,regression_nor,color ="orange",linewidth = 2,linestyle ="--",label = f"NOR deg:{round(slope_nor,4)}s/lap")

ax.set_title("VER vs SAI vs NOR Degradation Chart -- 2023 ITALIAN GP")
ax.set_xlabel("LapNumber")
ax.set_ylabel("LapTimeSeconds")
ax.legend()
ax.grid(True,alpha=0.3)

plt.savefig("outputs/monza_2023_degradation.png", dpi=150, bbox_inches="tight")
plt.tight_layout()
plt.show()



