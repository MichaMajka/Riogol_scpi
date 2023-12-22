import pyvisa
import time

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

# Close the connection
osciloscope.close()
