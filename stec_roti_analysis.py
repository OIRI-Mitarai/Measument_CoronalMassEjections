import georinex as gr
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 設定
# -----------------------------
rinex_obs_file = "OIRIbase.obs"
window_sec = 300
sampling_rate = 30

# -----------------------------
# 1. OBS 読み込み
# -----------------------------
obs = gr.load(rinex_obs_file)

# C1C または C1W を探す
code_types = [k for k in obs.keys() if k.startswith("C1")]
if len(code_types) == 0:
    raise ValueError("CANNOT FOUND pseudo-distance for the C1 series")
C1 = obs[code_types[0]]

# L1系
phase_types = [k for k in obs.keys() if k.startswith("L1")]
if len(phase_types) == 0:
    raise ValueError("CANNOT FOUND carrier phase of the L1 series")
L1 = obs[phase_types[0]]

# L1 波長
f1 = 1575.42e6
lambda1 = 3e8 / f1

# -----------------------------
# 2. STEC（簡易）計算
# -----------------------------
# 位相観測は cycles → meters に変換
L1_m = L1 * lambda1

# 掛け合わせて STEC proxy を作る（差分で良い）
# STEC = (L1 - C1): これは ionospheric delay + ambiguity
STEC = L1_m - C1

# -----------------------------
# 3. ROT = STEC の時間差分
# -----------------------------
ROT = STEC.diff(dim="time") / sampling_rate

# -----------------------------
# 4. ROTI = ROT の5分窓の標準偏差
# -----------------------------
window = int(window_sec / sampling_rate)

ROTI = ROT.rolling(time=window, center=True).std()

# -----------------------------
# 5. すべての衛星で平均ROTI
# -----------------------------
ROTI_mean = ROTI.mean(dim="sv")

# -----------------------------
# 6. NetCDF形式で保存
# -----------------------------
ROTI.to_netcdf("roti_output_CME.nc")

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
plt.show()
