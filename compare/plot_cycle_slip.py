import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from math import sqrt


def load_mw_csv(path):
    times = []
    values = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            times.append(datetime.fromisoformat(r["timestamp"]))
            values.append(float(r["mw"]))
    return times, values


def main():
    times_CME, mw_CME = load_mw_csv("output_mw_CME.csv")
    times_NORMAL, mw_NORMAL = load_mw_csv("output_mw_NORMAL.csv")

    fig, (axCME, axNOR) = plt.subplots(nrows=2, figsize=(12, 4))

    axCME.plot(times_CME, mw_CME, ".", ms=1)
    axCME.set_title("MW Time Series(CME)")
    axCME.set_xlabel("Time")
    axCME.set_ylabel("MW Combination (units)")
    axCME.grid()
    axCME.set_ylim(-350, 480)
    axCME.set_xlim(np.datetime64("2025-11-12T07:30"), np.datetime64("2025-11-12T19:30"))

    axNOR.plot(times_NORMAL, mw_NORMAL, ".", ms=1)
    axNOR.set_title("MW Time Series(NORMAL)")
    axNOR.set_xlabel("Time")
    axNOR.set_ylabel("MW Combination (units)")
    axNOR.grid()
    axNOR.set_ylim(-350, 480)
    axNOR.set_xlim(np.datetime64("2025-11-17T07:30"), np.datetime64("2025-11-17T19:30"))

    plt.show()


if __name__ == "__main__":
    main()
