import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()
print(rm.list_resources())

osciloscope = rm.open_resource('USB0::0x1AB1::0x04CE::DS1ZA224712323::INSTR')
print(osciloscope.query("*IDN?"))
osciloscope.write(':RUN')
osciloscope.timeout = 5000
time.sleep(0.1)

osciloscope.write(':MEASure:SOURce CHANnel1')
osciloscope.write(':MEASure:ITEM VMAX,CHANnel1')
osciloscope.write(":ACQUIRE:TYPE NORMAL")
osciloscope.write(":CHANNEL1:DISPLAY ON")
osciloscope.write(":TIMEBASE:SCALE 0.5")
osciloscope.write(":TRIGGER:EDGE:SOURCE CHANNEL1")
osciloscope.write(":TRIGGER:EDGE:MODE SINGLE")
osciloscope.write(":TRIGGER:EDGE:LEVEL 10")
osciloscope.write(":SINGLE")

# Wait and Check for Trigger
triggered = False
print("start measuring")
while not triggered:
    response = osciloscope.query(":TRIGger:POSition?").strip()
    if response != '-2':
        triggered = True
    else:
        time.sleep(0.1)  # Wait for a
time.sleep(1)
max_value_str = osciloscope.query(':MEASure:ITEM? VMAX,CHANnel1')
max_value_float = float(max_value_str.strip())
print(max_value_float)

# Capture the waveform data
osciloscope.write(":WAVEFORM:FORMAT ASCII")
osciloscope.write(":WAVEFORM:SOURCE CHANNEL1")
osciloscope.write(":WAVEFORM:MODE NORMAL")
raw_data = osciloscope.query(":WAVEFORM:DATA?")
header_length = 2 + int(raw_data[1])  # '#9' + number of digits in the length field
data_string = raw_data[header_length:]
waveform_data = np.array([float(val) for val in data_string.split(',')])



# Time per division and number of divisions (adjust these based on your oscilloscope settings)
time_per_div = 0.5  # seconds per division
num_divisions = 10  # total number of horizontal divisions on the screen
total_time = time_per_div * num_divisions
time_step = total_time / len(waveform_data)
times = np.arange(0, total_time, time_step)

# Find the indices where voltage crosses 5V and 10V
index_0v = np.where(waveform_data >= 0)[0][0]
index_5v = np.where(waveform_data >= 5)[0][0]
index_10v = np.where(waveform_data >= 10)[0][0]

# Calculate the time difference
time_0v = times[index_0v]
time_5v = times[index_5v]
time_10v = times[index_10v]
time_difference = time_10v - time_5v

print(f"Time from 5V to 10V: {time_difference} seconds")

# Plot the waveform
plt.figure(figsize=(10, 6))
plt.plot(times, waveform_data)
plt.title('Oscilloscope Waveform')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.show()

# Close the connection
osciloscope.close()
