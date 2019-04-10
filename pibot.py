"""
File: skidsteer_two_pwm_test.py

This code will test Raspberry Pi GPIO PWM on four GPIO
pins. The code test ran with L298N H-Bridge driver module connected.

Website:	www.bluetin.io
Date:		27/11/2017
"""

__author__ = "Mark Heywood"
__version__ = "0.1.0"
__license__ = "MIT"

from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from time import sleep
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 24
GPIO_ECHO = 18
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


#///////////////// Define Motor Driver GPIO Pins /////////////////
# Motor A, Left Side GPIO CONSTANTS
PWM_DRIVE_LEFT = 21		# ENA - H-Bridge enable pin
FORWARD_LEFT_PIN = 26	# IN1 - Forward Drive
REVERSE_LEFT_PIN = 19	# IN2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_DRIVE_RIGHT = 5		# ENB - H-Bridge enable pin
FORWARD_RIGHT_PIN = 13	# IN1 - Forward Drive
REVERSE_RIGHT_PIN = 6	# IN2 - Reverse Drive

# Initialise objects for H-Bridge GPIO PWM pins
# Set initial duty cycle to 0 and frequency to 1000
driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 1000)
driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 1000)

# Initialise objects for H-Bridge digital GPIO pins
forwardLeft = PWMOutputDevice(FORWARD_LEFT_PIN)
reverseLeft = PWMOutputDevice(REVERSE_LEFT_PIN)
forwardRight = PWMOutputDevice(FORWARD_RIGHT_PIN)
reverseRight = PWMOutputDevice(REVERSE_RIGHT_PIN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    dist = (TimeElapsed * 34300) / 2
    return dist

def allStop():
    forwardLeft.value = False
    reverseLeft.value = False
    forwardRight.value = False
    reverseRight.value = False
    driveLeft.value = 0
    driveRight.value = 0

def forwardDrive():
    forwardLeft.value = True
    reverseLeft.value = False
    forwardRight.value = True
    reverseRight.value = False
    driveLeft.value = 0.1
    driveRight.value = 0.1

def reverseDrive():
    forwardLeft.value = False
    reverseLeft.value = True
    forwardRight.value = False
    reverseRight.value = True
    driveLeft.value = 0.5
    driveRight.value = 0.5

def spinLeft():
    forwardLeft.value = False
    reverseLeft.value = True
    forwardRight.value = True
    reverseRight.value = False
    driveLeft.value = 1.0
    driveRight.value = 1.0

def SpinRight():
    forwardLeft.value = True
    reverseLeft.value = False
    forwardRight.value = False
    reverseRight.value = True
    driveLeft.value = 0.25
    driveRight.value = 0.25

def forwardTurnLeft():
    forwardLeft.value = True
    reverseLeft.value = False
    forwardRight.value = True
    reverseRight.value = False
    driveLeft.value = 0.2
    driveRight.value = 0.8

def forwardTurnRight():
    forwardLeft.value = True
    reverseLeft.value = False
    forwardRight.value = True
    reverseRight.value = False
    driveLeft.value = 0.8
    driveRight.value = 0.2

def reverseTurnLeft():
    forwardLeft.value = False
    reverseLeft.value = True
    forwardRight.value = False
    reverseRight.value = True
    driveLeft.value = 0.2
    driveRight.value = 0.8

def reverseTurnRight():
    forwardLeft.value = False
    reverseLeft.value = True
    forwardRight.value = False
    reverseRight.value = True
    driveLeft.value = 0.8
    driveRight.value = 0.2


if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if dist > 40:
                forwardDrive()
            elif dist < 40 or dist > 3000:
                allStop()
                time.sleep(1)
                reverseDrive() 
                time.sleep(0.5)
                allStop()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()