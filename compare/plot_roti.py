import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


ds = xr.load_dataset('output_roti_CME.nc')
ds = ds.rename({"__xarray_dataarray_variable__": "ROTI"})
ROTI_CME = ds["ROTI"]
ROTI_CME_mean = ROTI_CME.mean(dim="sv")

ds = xr.load_dataset('output_roti_NORMAL.nc')
ds = ds.rename({"__xarray_dataarray_variable__": "ROTI"})
ROTI_NORMAL = ds["ROTI"]
ROTI_NORMAL_mean = ROTI_NORMAL.mean(dim="sv")

# plt.figure(figsize=(14, 7))
fig, (axCME, axNOR) = plt.subplots(nrows=2, figsize=(14, 7))

# 各衛星の ROTI
for sv in ROTI_CME.sv.values:
    axCME.plot(ROTI_CME.time, ROTI_CME.sel(sv=sv), alpha=0.4, label=str(sv))

for sv in ROTI_NORMAL.sv.values:
    axNOR.plot(ROTI_NORMAL.time, ROTI_NORMAL.sel(sv=sv), alpha=0.4, label=str(sv))

# 平均ROTIを太線で
axCME.plot(ROTI_CME.time, ROTI_CME_mean, linewidth=3, color="black", label="Mean ROTI")
axNOR.plot(ROTI_NORMAL.time, ROTI_NORMAL_mean, linewidth=3, color="black", label="Mean ROTI")

axCME.set_title("ROTI for all satellites(CME)")
axCME.set_xlabel("Time")
axCME.set_ylabel("ROTI (TECU/min)")
axCME.grid(True)
# axCME.legend(ncol=8, fontsize=8, bbox_to_anchor=(0,1))
axCME.legend(ncol=14, fontsize=8, loc='upper left')
axCME.set_ylim(0,1.0)
axCME.set_xlim(np.datetime64("2025-11-12T07:30"), np.datetime64("2025-11-12T19:30"))

axNOR.set_title("ROTI for all satellites(NORMAL)")
axNOR.set_xlabel("Time")
axNOR.set_ylabel("ROTI (TECU/min)")
axNOR.grid(True)
# axNOR.legend(ncol=8, fontsize=8, bbox_to_anchor=(0,1))
axNOR.legend(ncol=14, fontsize=8, loc='upper left')
axNOR.set_ylim(0,1.0)
axNOR.set_xlim(np.datetime64("2025-11-17T07:30"), np.datetime64("2025-11-17T19:30"))

plt.tight_layout()
plt.show()
