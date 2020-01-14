#!/usr/bin/env python3

import csv

data = []

with open('swap-stats.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Omit header
    for row in reader:
        data.append((int(row[0]), float(row[1])))

start, p0 = data[0]
end, p1 = data[-1]

APR = (p1 / p0) ** (86400 * 365 / (end - start)) - 1

print(APR)
