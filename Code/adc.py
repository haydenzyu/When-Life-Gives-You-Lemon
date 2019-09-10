#Hayden Yu          
#9/1/19             
#ADC code for soil moisture sensor
#Followed freenove's ADC tutorial in documentation directory
#Sensor's manual is in the datasheet directory

import smbus
import time

address = 0x48 #address of PCF8591
bus = smbus.SMBus(1)
cmd = 0x40 #command
wet = 120
moist = 145
air = 200
water = 90

def analogRead(chn): #read ADC value from chn 0,1,2, or 3
    value = bus.read_byte_data(address, cmd+chn)
    return value

def loop():
    while True:
        value = analogRead(0) #read the ADC value of channel 0
        voltage = value/255.0 *3.3 #calculate the voltage value
        if value > wet and value <= moist:
            state = 'Good'
        elif value > moist:
            state = 'Need Water'
        else:
            state = 'Too wet'
        print('ADC value: %d, Voltage: %.2f, %s' %(value, voltage, state)) #print value to terminal
        time.sleep(1) #reads value every minute

def destroy():
    bus.close()

if __name__=='__main__':
    print('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
