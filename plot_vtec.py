import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import math


def load_vtec_csv(path="vtec_timeseries_CME.csv"):
    times = []
    values = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            times.append(datetime.fromisoformat(r["timestamp"]))
            values.append(float(r["vtec"]))
    return times, values


def plot_vtec(times, vtecs):
    plt.figure(figsize=(14, 7))
    plt.plot(times, vtecs, marker=".", linestyle="None")
    plt.title("VTEC Time Series")
    plt.xlabel("Time")
    plt.ylabel("ΔVTEC (TECU)")
    plt.grid(True)
    plt.ylim(-1800, 4800)
    plt.xlim(np.datetime64("2025-11-12T07:30"), np.datetime64("2025-11-12T19:30"))
    plt.show()


def main():
    times, vtecs = load_vtec_csv()
    plot_vtec(times, vtecs)


if __name__ == "__main__":
    main()
