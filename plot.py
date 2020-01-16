#!/usr/bin/env python3
import csv
import numpy as np
from datetime import datetime


def plot_profit(data):
    import matplotlib.pyplot as plt
    import math

    # Configure matplotlib for publication quality
    # http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples
    # thesis: 345
    fig_width_pt = 350
    inches_per_pt = 1.0/72.27               # Convert pt to inches
    golden_mean = (math.sqrt(5)-1.0)/2.0         # Aesthetic ratio
    fig_width = fig_width_pt * inches_per_pt  # width in inches
    fig_height = fig_width * golden_mean       # height in inches
    fig_size = [fig_width, fig_height]
    params = {
        'backend': 'ps',
        'axes.labelsize': 8,
        'axes.linewidth': 0.35,
        'font.family': 'serif',
        'font.size': 8,
        'legend.fontsize': 7,
        'xtick.labelsize': 6,
        'ytick.labelsize': 6,
        'xtick.major.size': 2,
        'ytick.major.size': 2,
        'text.usetex': False,
        'figure.figsize': fig_size,
        'lines.linewidth': 0.7,
        'lines.markeredgewidth': 0.2,
    }
    plt.rcParams.update(params)
    plt.figure(1)
    plt.clf()
    a = 0.13
    b = 0.13
    plt.axes([a, b, 0.98-a, 0.99-b])

    t, p = data[:, 0], data[:, 1]
    dt = t.max() - t.min()
    dp = p.max() - p.min()
    plt.plot(t, p, c='blue')
    plt.xlim(t.min() - dt * 0.05, t.max() + dt * 0.05)
    plt.ylim(p.min() - dp * 0.05, p.max() + dp * 0.05)
    plt.xlabel('time')
    plt.ylabel('virtual price ($)')
    plt.savefig('profit.png', dpi=300)


def read_data():
    data = []
    with open('swap-stats.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Omit header
        for row in reader:
            data.append((datetime.fromtimestamp(int(row[0])), float(row[1])))
    return np.array(data)


if __name__ == '__main__':
    plot_profit(read_data())
