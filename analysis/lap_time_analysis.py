"""
F1 Lap Time Analysis
2023 British GP (Silverstone) — HAM vs VER vs NOR
Lap time evolution across full race distance.
"""

import fastf1
import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("f1_cache",exist_ok=True)
fastf1.Cache.enable_cache("f1_cache")

session = fastf1.get_session(2023,"Great Britain","R")
session.load()
laps = session.laps
#Filter Drivers
hamilton_laps = laps.pick_drivers("HAM").copy()
verstappen_laps = laps.pick_drivers("VER").copy()
norris_laps = laps.pick_drivers("NOR").copy()
#LapTime
hamilton_laps["LapTimeSeconds"] = hamilton_laps["LapTime"].dt.total_seconds()
verstappen_laps["LapTimeSeconds"] = verstappen_laps["LapTime"].dt.total_seconds()
norris_laps["LapTimeSeconds"] = norris_laps["LapTime"].dt.total_seconds()
#Filter out outliers (e.g. pit stops, safety car laps)
ham_clean = hamilton_laps[hamilton_laps["LapTimeSeconds"] < 105]
ver_clean = verstappen_laps[verstappen_laps["LapTimeSeconds"] < 105]
nor_clean = norris_laps[norris_laps["LapTimeSeconds"] < 105]
#Plot
fig , ax = plt.subplots(figsize=(12,6))

ax.plot(ham_clean["LapNumber"],ham_clean["LapTimeSeconds"],label="HAM",color="cyan")
ax.plot(ver_clean["LapNumber"],ver_clean["LapTimeSeconds"],label="VER",color="red")
ax.plot(nor_clean["LapNumber"],nor_clean["LapTimeSeconds"],label="NOR",color="orange")

ax.set_title("Lap Time Evolution - 2023 British GP")
ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time (Seconds)")
ax.legend()
ax.grid(True,alpha=0.3)

plt.savefig("outputs/british_gp_2023_lap_times.png", dpi=150, bbox_inches="tight")
plt.tight_layout()
plt.show()
