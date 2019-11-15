#Hayden Yu          
#9/1/19             
#ADC code for soil moisture sensor
#Followed freenove's ADC tutorial in documentation directory
#Sensor's manual is in the datasheet directory

import smbus
import time
import RPi.GPIO as GPIO

address = 0x48 #address of PCF8591
bus = smbus.SMBus(1)
cmd = 0x40 #command
wet = 120
moist = 145
air = 200
water = 90
relayPin = 38
one_day = 86400 #seconds in a day

def setup():
    print('Program is starting...')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(relayPin, GPIO.OUT)

def analogRead(chn): #read ADC value from chn 0,1,2, or 3
    value = bus.read_byte_data(address, cmd+chn)
    return value

def loop():
    while(1):
        time.sleep(1)
        GPIO.output(relayPin, True)
        time.sleep(3)
        GPIO.output(relayPin, False)

def destroy():
    GPIO.output(relayPin, False)
    GPIO.cleanup()
    bus.close()

if __name__=='__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
