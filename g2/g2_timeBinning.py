import matplotlib
# matplotlib.use('TkAgg')  # Set the backend to TkAgg

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# mpl.use('macosx')

# Read the CSV file
filepath = 'F:/Users/QPG/Documents/zerui_g15/C-hBN_new/g2/23_04_25.csv'
# filepath = "G:/g2/2025-04-29.csv"
data = pd.read_csv(filepath, header=None, names=['Value'])
data['Value'] = pd.to_numeric(data['Value'], errors='coerce')  # Convert to numeric, non-convertible values become NaN

# Create a time axis (in picoseconds)
# time = np.arange(0, len(data) * 128, 128)
time = np.arange(0, 60000, 128)/1000
data = data['Value'][:len(time)]

time = time[1:]
data = data[1:]

print(data)

# time binning
def selective_time_bin(time, values, bin_size=2, center_start=None, center_end=None):
    if center_start is None or center_end is None:
        center_start = len(values) // 3
        center_end = 2 * len(values) // 3

    binned_time = []
    binned_values = []

    # First region
    for i in range(0, center_start, bin_size):
        bin_end = min(i + bin_size, center_start)
        binned_time.append(np.mean(time[i:bin_end]))
        binned_values.append(np.mean(values[i:bin_end]))

    # Center region (no binning)
    binned_time.extend(time[center_start:center_end])
    binned_values.extend(values[center_start:center_end])

    # Last region
    for i in range(center_end, len(values), bin_size):
        bin_end = min(i + bin_size, len(values))
        binned_time.append(np.mean(time[i:bin_end]))
        binned_values.append(np.mean(values[i:bin_end]))

    return np.array(binned_time), np.array(binned_values)



def exponential_func(x, a, b, c, d):
    return a * np.exp(b * np.abs(x-c)) + d


p0 = np.array([-30, -1, 30, 50])
popt, pcov = curve_fit(exponential_func, time, data, p0=p0)

data = data / exponential_func(time[-1], *popt)
popt, pcov = curve_fit(exponential_func, time, data, p0=p0)
print("g2(0) = ", np.min(exponential_func(time, *popt)))

centerWidth=5.5
bin_size = 4

left_end = popt[2] - centerWidth/2
right_start = popt[2] + centerWidth/2
binned_time, binned_data = selective_time_bin(time, data, bin_size=bin_size, center_start=int(np.where(time < left_end)[0][-1]), center_end=int(np.where(time > right_start)[0][0]))

time = time - popt[2]
binned_time = binned_time - popt[2]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.axvspan(left_end - popt[2], right_start - popt[2], facecolor='red', alpha=0.2)
ax.plot(binned_time, binned_data, 'ko', label='data')
ax.plot(time, exponential_func(time + popt[2], *popt), 'r', label='exponential fit')
ax.set_xlabel(r'$\tau$ (ns)', fontsize=16)
ax.set_ylabel(r'$g^{2}(\tau)$', fontsize=16)
# ax.set_title('g2 data with exponential fit')
ax.set_xlim(-10,10)
ax.grid(True)
ax.legend(fontsize=14)

# Show the plot
plt.tick_params(axis='both', which='major', labelsize=14)
plt.show()