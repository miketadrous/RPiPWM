#Libraries
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set GPIO Pins
GPIO_LED=18
GPIO_TRIGGER = 23
GPIO_ECHO = 24

 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)

PWM=GPIO.PWM(GPIO_LED,100)

PWM.start(0)


def distance():
    
    StartTime = time.time()
    StopTime = time.time()
    
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime

    distance = (TimeElapsed * 34300) / 2
 
    return distance

try:
    while True:
        dist = distance()
        print ("Distance = %.1f cm" % dist)
            
        if (dist<=50):
            PWM.ChangeDutyCycle((50-dist)*2)
            time.sleep(0.005)
                
        else:
            PWM.ChangeDutyCycle(0)
                
        time.sleep(1)

 
#pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    PWM.stop()
    GPIO.cleanup()
        
