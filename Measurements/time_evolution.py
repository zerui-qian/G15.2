# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 15:49:46 2025

@author: QPG
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time  # To track elapsed time
import sys
sys.path.append(r'F:/Users/QPG/Documents/zerui_g15/C-hBN_new/Devices')
from DeviceManager import *
#%%
#-------------------------------------APD-------------------------------------#
times = []  # Stores absolute time values
counts = []  # Stores count rate values
start_time = time.time()  # Reference start time

fig, ax = plt.subplots(figsize=(8, 4))
line, = ax.plot([], [], 'r-', label="Count Rate (Hz)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Count Rate (Hz)")
ax.set_title("Live Count Rate Monitor")
ax.grid(True)

def update(frame):
    current_time = time.time() - start_time  # Elapsed time "since start
    new_count = ph.GetCountRate()  

    # Append new values
    times.append(current_time)
    counts.append(new_count)
    line.set_data(times, counts)

    # Auto-rescale axes
    ax.relim()  # Recalculate limits based on new data
    ax.autoscale_view()  # Rescale the view to fit new limits

    return line,

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()

#%%-------------------------------laser_power---------------------------------#
times = []  # Stores absolute time values
counts = []  # Stores count rate values
start_time = time.time()  # Reference start time

fig, ax = plt.subplots(figsize=(8, 4))
line, = ax.plot([], [], 'r-', label="P_in")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Power (mW)")
ax.set_title("Live Laser Power Monitor")
ax.grid(True)

def update(frame):
    current_time = time.time() - start_time  # Elapsed time since start
    new_count = 0.55*NIDAQ.ai0()

    # Append new values
    times.append(current_time)
    counts.append(new_count)
    line.set_data(times, counts)

    # Auto-rescale axes
    ax.relim()  # Recalculate limits based on new data
    ax.autoscale_view()  # Rescale the view to fit new limits

    return line,

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()

#%%
# # Initialize data storage
# times = []
# counts_apd = []
# powers = []

# start_time = time.time()  # Reference start time

# # Create subplots: APD (top), Power (bottom)
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
# fig.subplots_adjust(hspace=0.3)

# # APD Count Plot (Top)
# line1, = ax1.plot([], [], 'r-', label="Count Rate (Hz)")
# ax1.set_ylabel("APD Count Rate (Hz)")
# ax1.set_title("Live Monitoring")
# ax1.grid(True)
# ax1.legend()

# # Power Plot (Bottom)
# line2, = ax2.plot([], [], 'b-', label="Laser Power (mW)")
# ax2.set_xlabel("Time (s)")
# ax2.set_ylabel("Power (mW)")
# ax2.grid(True)
# ax2.legend()

# def update(frame):
#     current_time = time.time() - start_time
#     count_rate = ph.GetCountRate()
#     power = 5 * NIDAQ.ai0()

#     # Append new data
#     times.append(current_time)
#     counts_apd.append(count_rate)
#     powers.append(power)

#     # Update APD plot
#     line1.set_data(times, counts_apd)
#     ax1.relim()
#     ax1.autoscale_view()

#     # Update Power plot
#     line2.set_data(times, powers)
#     ax2.relim()
#     ax2.autoscale_view()

#     return line1, line2

# ani = animation.FuncAnimation(fig, update, interval=100)
# plt.show()

#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import csv
import os
import sys
sys.path.append(r'F:/Users/QPG/Documents/zerui_g15/C-hBN_new/Devices')
from DeviceManager import *

# Create output file with timestamp
timestamp_str = time.strftime("%Y%m%d_%H%M%S")
save_path = f"Z:\Projects\Defects for QTM\Raw_data_zerui\Power_dep\{timestamp_str}.csv"

# Write header
with open(save_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Elapsed Time (s)', 'Power (mW)', 'APD Count Rate (Hz)'])

# Data storage
times = []
powers = []
counts_apd = []

start_time = time.time()

# Set up figure
fig, ax = plt.subplots(figsize=(7, 5))
sc = ax.plot([], [], 'ro', label='APD vs Power')[0]
ax.set_xlabel("Laser Power (mW)")
ax.set_ylabel("APD Count Rate (Hz)")
ax.set_title("Live: APD Counts vs Laser Power")
ax.grid(True)
ax.legend()

def update(frame):
    current_time = time.time() - start_time
    power = 0.55 * NIDAQ.ai0()
    count_rate = ph.GetCountRate()

    times.append(current_time)
    powers.append(power)
    counts_apd.append(count_rate)

    # Update plot
    sc.set_data(powers, counts_apd)
    ax.relim()
    ax.autoscale_view()

    # Append to CSV
    with open(save_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([current_time, power, count_rate])

    return sc,

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()

#%%
data = np.loadtxt(r"Z:\\Projects\\Defects for QTM\\Raw_data_zerui\\Power_dep\\20250504_181658.csv", skiprows=1, delimiter=',')
P = data[:, 1]
Counts = data[:, 2]

plt.plot(P, Counts, 'ro')
plt.show()