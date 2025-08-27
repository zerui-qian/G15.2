# -*- coding: utf-8 -*-
"""
Created on Thu Nov 7 2024

@program: Measurement Controller
@functionality: This script allows to start various measurements.
"""
from DeviceManager import *
import polarization
import APDscanAttocube
import spectrum
import save
import sys
import os
sys.path.append(os.path.abspath(r'Devices'))
sys.path.append(os.path.abspath(r'Logging'))
sys.path.append(os.path.abspath(r'Measurements'))


# Configuration Section
measure_dummyAPDscan = 0
measure_APDscan = 0
measure_PLE = 0
measure_spectrum = 1
measure_APDScanAttocube = 0
measure_polarization = 0

general_params = {
    'sample_code': '23-09-2024-hBN',
    'chip': 2,
    'flake': 18,
    'excitation_power (mW)': 0.66,
    'excitation_wavelength': 520,
    'temperature': 4,
    'setup': 'BC5',
    'flake thickness (nm)': "?",
}

# Parameters for each measurement type


# APD_SCAN_ATTOCUBE_PARAMS = {
#     "measurement": "APD_scan_attocube",
#     "x_step": 1,
#     "y_step": 1,
#     "x_number": int(20),
#     "y_number": int(20),
#     "x_start": 65,
#     "y_start": 60,
#     "stop_counts": 20e4,
#     "single_direction": True,
#     "live_plot": True
# }

APD_SCAN_ATTOCUBE_PARAMS = {
    "measurement": "APD_scan_attocube",
    "x_step": 1,
    "y_step": 1,
    "x_number": int(50),
    "y_number": int(50),
    "x_start": 0,
    "y_start": 0,
    "stop_counts": 10e4,
    "single_direction": True,
    "live_plot": True
}


SPECTRUM_PARAMS = {
    "measurement": "spectrum",
    "integration_time": 60*5
}


POL_PARAMS = {
    'measurement': 'polarization',
    'spec': True,
    'the_num': 360}


def main(DM):
    # Run the selected measurement
    log = general_params.copy()

    if measure_spectrum:
        print("Starting spectrum measurement")
        data = spectrum.spectrum(SPECTRUM_PARAMS, location='G15')
        log.update(SPECTRUM_PARAMS)

    elif measure_APDScanAttocube:
        print("Starting Attocube APD scan")
        print(f"DeviceManager ID in main: {id(DM)}")
        data = APDscanAttocube.scan_area(APD_SCAN_ATTOCUBE_PARAMS)
        log.update(APD_SCAN_ATTOCUBE_PARAMS)

    elif measure_polarization:
        print("Starting polarization measurement")
        data = polarization.scan_angle(POL_PARAMS)
        log.update(POL_PARAMS)

    else:
        print("Unknown measurement type")

    if data != None:
        save.save_measurement(data, log)
    print("Measurement complete.")
    return DM


if __name__ == "__main__":
    main(DM)
