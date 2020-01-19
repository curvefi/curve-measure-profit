#!/usr/bin/env python3

import csv
import json

day = 86400
week = 7 * day

data = []
output = {}

with open('swap-stats.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Omit header
    for row in reader:
        data.append((int(row[0]), float(row[1])))

start, p0 = data[0]
end, p1 = data[-1]

start_week, p_week = next((t, p) for (t, p) in data if t >= end - week)
start_day, p_day = next((t, p) for (t, p) in data if t >= end - day)

apr = (p1 / p0) ** (365 * day / (end - start)) - 1
weekly_apr = (p1 / p_week) ** (365 * day / (end - start_week)) - 1
daily_apr = (p1 / p_day) ** (365 * day / (end - start_day)) - 1

output['apr'] = apr
output['daily_apr'] = daily_apr
output['weekly_apr'] = weekly_apr
output['data'] = data

with open('stats.json', 'w') as f:
    json.dump(output, f)
