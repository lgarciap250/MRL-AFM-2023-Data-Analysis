import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# use latex for font rendering, use serif font
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# change font size to 6 for legend
plt.rcParams.update({'font.size': 11})

# Define the paths to the data
data_paths = [
    "C:\\Users\\AFM\\Dropbox\\Qatar 3D Printing\\Reports\\report-data-dump\\data-log-[15-03-28]-experiment",
    "C:\\Users\\AFM\\Dropbox\\Qatar 3D Printing\\Reports\\report-data-dump\\data-log-[15-04-57]-experiment",
    "C:\\Users\\AFM\\Dropbox\\Qatar 3D Printing\\Reports\\report-data-dump\\data-log-[15-06-38]-experiment",
    "C:\\Users\\AFM\\Dropbox\\Qatar 3D Printing\\Reports\\report-data-dump\\data-log-[15-46-26]-experiment",
    "C:\\Users\\AFM\\Dropbox\\Qatar 3D Printing\\Reports\\report-data-dump\\data-log-[15-45-36]-experiment",
    "C:\\Users\\AFM\\Dropbox\\Qatar 3D Printing\\Reports\\report-data-dump\\data-log-[15-44-18]-experiment",
    "C:\\Users\\AFM\\Dropbox\\Qatar 3D Printing\\Reports\\report-data-dump\\data-log-[15-42-03]-experiment"
]

# Define the loop delay in seconds
loop_delay = 0.01  # 10ms

# Set up the subplot figure
fig, axs = plt.subplots(7, 1)


# Loop over the data paths
for i, data_path in enumerate(data_paths):

    # Get the pressure setting from the data path
    pressure_setting = float(os.listdir(data_path)[0].split('=')[1].split('.csv')[0])

    # Load the data
    data = pd.read_csv(os.path.join(data_path, os.listdir(data_path)[0]),delimiter=',',skiprows=1,header=None)
    
    # Compute the time for pressure to go from 0.2 psi back to 0 psi
    transition_start = data[(data.iloc[:, 2] == 0) & (data.iloc[:, 2].shift(1) == pressure_setting)].index[0]
    settling_data = data[transition_start:]
    settling_time_idx = settling_data[(settling_data.iloc[:, 0] <= 0.05 * 0.2)].index[0]
    settling_time = (settling_time_idx - transition_start) * loop_delay

    # Create time variable for plotting
    time = (data.iloc[:, 1]) * loop_delay
    time = time - time[transition_start]

    # Set ylabel for the first subplot only
    if i == 3:
        axs[i].set_ylabel('Pressure (psi)')
        axs[i].set_yticks([0,0.25])
    else:
        axs[i].set_yticks([])
        axs[i].set_yticklabels([])

    # Plotting the data
    axs[i].plot(time, data.iloc[:, 0], label=f'Pressure Reading, Transition Time: {settling_time} s')
    axs[i].plot(time, data.iloc[:, 2], label='Command Pressure')
    # axs[i].set_ylim([0, 0.25])
    axs[i].set_xlim([0,30])
    axs[i].legend()


plt.xlabel('Time (s)')
plt.tight_layout()

# Remove vertical space between subplots
plt.subplots_adjust(hspace=-0.02)

plt.show()
