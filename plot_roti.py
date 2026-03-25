import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# ROTI = xr.load_dataset("roti_output_CME.nc")["ROTI"]
# ROTI_mean = ROTI.mean(dim="sv")

ds = xr.load_dataset('roti_output.nc')
print(ds)

ds = ds.rename({"__xarray_dataarray_variable__": "ROTI"})
ROTI = ds["ROTI"]

ROTI_mean = ROTI.mean(dim="sv")

# -----------------------------
# 7. プロット
# -----------------------------
plt.figure(figsize=(14, 7))

# 各衛星の ROTI
for sv in ROTI.sv.values:
    plt.plot(ROTI.time, ROTI.sel(sv=sv), alpha=0.4, label=str(sv))

# 平均ROTIを太線で
plt.plot(ROTI.time, ROTI_mean, linewidth=3, color="black", label="Mean ROTI")

plt.title("ROTI for all satellites")
plt.xlabel("Time")
plt.ylabel("ROTI (TECU/min)")
plt.grid(True)
plt.legend(ncol=4, fontsize=8)
plt.tight_layout()
plt.ylim(0,1.0)
plt.xlim(np.datetime64("2025-11-12T07:30"), np.datetime64("2025-11-12T19:30"))
plt.tight_layout()
plt.show()
