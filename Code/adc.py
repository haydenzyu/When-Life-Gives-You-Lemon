import smbus
import time

address = 0x48 #address of PCF8591
bus = smbus.SMBus(1)
cmd = 0x40 #command

def analogRead(chn): #read ADC value from chn 0,1,2, or 3
    value = bus.read_byte_data(address, cmd+chn)
    return value

def loop():
    while True:
        value = analogRead(0) #read the ADC value of channel 0
        voltage = value/255.0 *3.3 #calculate the voltage value
        print('ADC value: %d, Voltage: %.2f' %(value, voltage))
        time.sleep(1)

def destroy():
    bus.close()

if __name__=='__main__':
    print('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
