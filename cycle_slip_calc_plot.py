import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from math import sqrt

c = 299792458.0
f_gps_L1 = 1575.42e6
f_gps_L2 = 1227.60e6
f_glo_L1 = 1602e6
f_glo_L2 = 1246e6

lam_gps_L1 = c / f_gps_L1
lam_gps_L2 = c / f_gps_L2

# GLONASS FDMA周波数補正
def glo_freq(n):
    return 1602e6 + n * 0.5625e6


def parse_rinex3_obs(file):
    sys_obs = {}
    glo_slot = {}
    with open(file, "r") as f:
        # ---- header ----
        for line in f:
            if "SYS / # / OBS TYPES" in line:
                sys = line[0]
                n = int(line[3:6])
                types = line[7:].split()
                sys_obs[sys] = types

            if "GLONASS SLOT / FRQ" in line:
                m = re.findall(r"R(\d+)\s+(-?\d+)", line)
                for sat, frq in m:
                    glo_slot["R"+sat] = int(frq)

            if "END OF HEADER" in line:
                break

        # ---- data ----
        epochs = []
        sats = []
        obs_data = []

        for line in f:
            if line.startswith(">"):
                parts = line.split()
                y, mo, d, h, mi, sec = map(float, parts[1:7])
                cur_time = datetime(int(y), int(mo), int(d), int(h), int(mi), int(sec))
            else:
                sat = line[:3]
                system = sat[0]

                if system not in sys_obs:
                    continue

                types = sys_obs[system]
                values = {}

                # 分割ベースの RINEX3 形式
                items = re.findall(r'[- ]\d+\.\d+| {14}', line[3:])
                for t, v in zip(types, items):
                    try:
                        values[t] = float(v)
                    except:
                        values[t] = None

                epochs.append(cur_time)
                sats.append(sat)
                obs_data.append(values)

    return epochs, sats, obs_data, sys_obs, glo_slot


def mw_for_sat(system, sat, obs, glo_slot):
    # ---- GPS ----
    if system == "G":
        try:
            C1 = obs["C1C"]
            C2 = obs["C2L"]
            L1 = obs["L1C"]
            L2 = obs["L2L"]
        except KeyError:
            return None

        lam1 = lam_gps_L1
        lam2 = lam_gps_L2

    # ---- GLONASS ----
    elif system == "R":
        try:
            C1 = obs["C1C"]
            C2 = obs["C2C"]
            L1 = obs["L1C"]
            L2 = obs["L2C"]
        except KeyError:
            return None

        k = glo_slot.get(sat, 0)
        f1 = 1602e6 + 0.5625e6 * k
        f2 = 1246e6 + 0.4375e6 * k
        lam1 = c / f1
        lam2 = c / f2

    # ---- Other systems → MW 計算不可 ----
    else:
        return None

    # 値が None（欠損）なら MW 計算不可
    if any(v is None for v in [C1, C2, L1, L2]):
        return None

    # MW計算
    L1_m = L1 * lam1
    L2_m = L2 * lam2

    mw = (C1 - C2) / (lam1 - lam2) - (L1_m - L2_m)
    return mw


def main():
    file = "OIRIbase.obs"

    epochs, sats, obs_data, sys_obs, glo_slot = parse_rinex3_obs(file)

    mw_series = []
    times = []

    for t, sat, obs in zip(epochs, sats, obs_data):
        system = sat[0]
        mw = mw_for_sat(system, sat, obs, glo_slot)
        if mw is not None:
            mw_series.append(mw)
            times.append(t)

    # CSV保存
    with open("mw_series.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "mw"])
        for t, v in zip(times, mw_series):
            w.writerow([t.isoformat(), v])

    # 簡易プロット
    plt.plot(times, mw_series, ".", ms=2)
    plt.title("MW Time Series")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
