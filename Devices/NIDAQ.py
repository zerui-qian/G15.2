# -*- coding: utf-8 -*-
"""
Class for National Instruments DAQ Device unsing PyDAQmx wrapper for c dll.

NI-DAQmx C Reference Help
http://zone.ni.com/reference/en-XX/help/370471AA-01/

Synchronization Concept
http://www.ni.com/product-documentation/4322/en/#toc3

PyDAQmx Doc (very limited)
https://pythonhosted.org/PyDAQmx/index.html

Header file of dll and c examples are valuable to understand DAQmx.

TODO:
There are still exceptions (KeyBoardInterrupt during measurement or data 
reading?) that leave the daq card in a weird state after exiting this code. 
Some buffer stays non-empty and screws up the following measurements...

@author: Patrick Knüppel
@author: Yuya Shimazaki
"""

""" 
Specifications USB-6366
input ranges 10, 5, 2, 1V

"""

import numpy as np
import time
import nidaqmx
from nidaqmx.constants import Edge, AcquisitionType
import sys
sys.path.append(r'F:/Users/QPG/Documents/zerui_g15/C-hBN_new/pyro_nw')
import nw_utils as nw_utils

class NIDAQ:
    def __init__(self, device='Dev1/'):
        self.device_name = device
        self._ao0 = None
        self._ao1 = None
        self.output_handle = sys.stdout
        
    @property
    def ao0(self):
        return self._ao0

    @property
    def ao1(self):
        return self._ao1

    def set_ao0(self, voltage):
        """Set voltage going to nf power setpoint. Takes 3.1 ms!."""
        with nidaqmx.Task() as vTask:
            vTask.ao_channels.add_ao_voltage_chan(self.device_name + 'ao0', min_val=0, max_val=5)
            vTask.write(voltage, auto_start=True)
            vTask.stop()
        self._ao0 = voltage


    def set_ao1(self, voltage):
        """Set voltage going to FPGA AI0. Takes 3.1 ms!."""
        with nidaqmx.Task() as vTask:
            vTask.ao_channels.add_ao_voltage_chan(self.device_name + 'ao1', min_val=0, max_val=5)
            vTask.write(voltage, auto_start=True)
            vTask.stop()
        self._ao1 = voltage
    
    def smooth_set_ao0(self, target_value, step_size=0.01, delay=0.05):
        """
        Written by Johannes on December 15, 2024
        Smoothly sets ao0 from its current value to the target value.
        
        Parameters:
            target_value (float): The value to set ao0 to.
            step_size (float): The increment size for each step.
            delay (float): The time (in seconds) to wait between each step.
        """
        current_value = self.ao0
        direction = 1 if target_value > current_value else -1
        total_steps = int(abs(target_value - current_value) / step_size)

        for _ in range(total_steps):
            current_value += direction * step_size
            self.set_ao0(current_value, rate=0)
            time.sleep(delay)

        self.set_ao0(target_value)  # Ensure the final value is set accurately
    
    def ai0(self, samples=100, rate=1000):
        """
        Measures the voltage on AI0.
        
        Parameters:
            samples (int): Number of samples to take.
            rate (int): Sampling rate in Hz.
        
        Returns:
            float: The average voltage measured on AI0.
        """
        with nidaqmx.Task() as vTask:
            vTask.ai_channels.add_ai_voltage_chan(self.device_name + 'ai0', min_val=-10, max_val=10)
            vTask.timing.cfg_samp_clk_timing(rate, sample_mode=AcquisitionType.FINITE, samps_per_chan=samples)
            
            data = vTask.read(number_of_samples_per_channel=samples)
        
        return np.mean(data)
    
if __name__ == '__main__':
    object_dict = {
        'NIDAQ': NIDAQ(),
        }
    nw_utils.RunServer(object_dict)