# -*- coding: utf-8 -*-
"""
Created on Thu Dec  12 10:52:52 2024

@author: Johannes Eberle
"""

import numpy as np
import time
import sys
import os
sys.path.append(os.path.abspath(r'F:/Users/QPG/Documents/zerui_g15/C-hBN_new/Devices'))
from DeviceManager import *
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from pylablib.devices import Attocube

# Experiment parameters
# wait_time = 0.1  # Wait time in seconds
# wait_time = 0.15  # Wait time in seconds
wait_time = 0.05



def scan_angle(params):
    the_num = params.get("the_num")
    spec = params.get("spec")
    print(params)
    
    angles, counts = [], []
    for the in np.linspace(0, 180, the_num):
        ELL1.set_angle(the)
        angles.append(the)
        time.sleep(wait_time)
        
        apd_counts = ph.GetCountRate()
        counts.append(apd_counts)
    
    data = {
        'angles': np.array(angles),
        'apd_counts': np.array(counts),
        'wait_time': wait_time,
        'additional_info': 'Include any other relevant metadata here',
    }

    return data