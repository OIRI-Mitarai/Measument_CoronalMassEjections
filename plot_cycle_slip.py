import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from math import sqrt


def load_mw_csv(path="mw_series.csv"):
    times = []
    values = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            times.append(datetime.fromisoformat(r["timestamp"]))
            values.append(float(r["mw"]))
    return times, values


def main():
    times, mw = load_mw_csv()
    plt.plot(times, mw, ".", ms=2)
    plt.title("MW Time Series")
    plt.grid()
    plt.ylim(-350, 480)
    plt.xlim(np.datetime64("2025-11-12T07:30"), np.datetime64("2025-11-12T19:30"))
    plt.show()


if __name__ == "__main__":
    main()
