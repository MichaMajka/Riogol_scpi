import pyvisa
import time

rm = pyvisa.ResourceManager()
print(rm.list_resources())

osciloscope = rm.open_resource('USB0::0x1AB1::0x04CE::DS1ZA224712323::INSTR')
osciloscope.write(':STOP')
osciloscope.timeout = 5000
time.sleep(0.1)


osciloscope.write(':MEASure:SOURce CHANnel1')
time.sleep(0.1)
print(osciloscope.write(':MEASure:SOURce?'))

#osciloscope.write(':MEASure:ADISplay ON') measure all

# Set the measurement type to Maximum
osciloscope.write(':MEASure:ITEM VMAX,CHANnel1')
time.sleep(0.1)

# Query the maximum value
max_value = osciloscope.query(':MEASure:ITEM? VMAX,CHANnel1')
time.sleep(0.1)
print(f"Maximum value: {max_value}")



# Close the connection
osciloscope.close()
