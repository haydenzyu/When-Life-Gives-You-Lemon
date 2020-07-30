#Hayden Yu          
#9/1/19             
#ADC code for soil moisture sensor
#Followed freenove's ADC tutorial in documentation directory
#Sensor's manual is in the datasheet directory

import smbus
import time
import RPi.GPIO as GPIO
import datetime

address = 0x48 #address of PCF8591
bus = smbus.SMBus(1)
cmd = 0x40 #command
wet = 90
moist = 115
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
    GPIO.output(relayPin, False)
    while True:
        for int in range(5):
            value = analogRead(0) #read the ADC value of channel 0
            value2 = analogRead(1)
        voltage = (value+value2)/255.0 *3.3 #calculate the voltage value
        average = (value+value2)/2
        
        if average > wet and average <= moist:
            state = 'Good'
            GPIO.output(relayPin, False)
        elif average > moist:
            state = 'Need Water'
            f = open("output.txt", "a+")
            currentDT = datetime.datetime.now()
            print('ADC value: %d, Voltage: %.2f, %s' %(average, voltage, state)) #print value to terminal
            f.write("Water at %s, %s\n" %(str(currentDT), str(average))) 
            time.sleep(2)
            GPIO.output(relayPin, True)
            time.sleep(8)
            GPIO.output(relayPin, False)
            time.sleep(2)
            for int in range(5):
                value = analogRead(0) #read the ADC value of channel 0
                value2 = analogRead(1)
                time.sleep(2)
            average = (value+value2)/2
            print('ADC value: %d, Voltage: %.2f, %s' %(average, voltage, state)) #print value to terminal
            f.close()
        else:
            state = 'Too wet'
            GPIO.output(relayPin, False)
            
        print('ADC value: %d, Voltage: %.2f, %s' %(average, voltage, state)) #print value to terminal
        
        time.sleep(1)
        #print(value, value2)
    
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
