import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import math


def load_vtec_csv(path):
    times = []
    values = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            times.append(datetime.fromisoformat(r["timestamp"]))
            values.append(float(r["vtec"]))
    return times, values


def main():
    times_cme, vtecs_cme = load_vtec_csv("output_vtec_CME.csv")
    times_normal, vtecs_normal = load_vtec_csv("output_vtec_NORMAL.csv")

    fig, (axCME, axNOR) = plt.subplots(nrows=2, figsize=(12, 4))

    axCME.plot(times_cme, vtecs_cme, marker=".", linestyle="None")
    axCME.set_title("VTEC Time Series(CME)")
    axCME.set_xlabel("Time")
    axCME.set_ylabel("VTEC (TECU)")
    axCME.grid(True)
    axCME.set_ylim(-1800, 4800)
    axCME.set_xlim(np.datetime64("2025-11-12T07:30"), np.datetime64("2025-11-12T19:30"))

    axNOR.plot(times_normal, vtecs_normal, marker=".", linestyle="None")
    axNOR.set_title("VTEC Time Series(NORMAL)")
    axNOR.set_xlabel("Time")
    axNOR.set_ylabel("VTEC (TECU)")
    axNOR.grid(True)
    axNOR.set_ylim(-1800, 4800)
    axNOR.set_xlim(np.datetime64("2025-11-17T07:30"), np.datetime64("2025-11-17T19:30"))

    plt.show()

if __name__ == "__main__":
    main()
