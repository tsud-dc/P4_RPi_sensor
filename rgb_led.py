#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

pins = {'r':33, 'g':36, 'b':31}  # pins is a dict

def rgb_init(pins):
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
        GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

def turn_on(pins, *color):
    for col in color:
        GPIO.output(pins[col], GPIO.LOW)

def turn_off(pins, *color):
    for col in color:
        GPIO.output(pins[col], GPIO.HIGH)

def gpio_cleanup():
    GPIO.cleanup()

def rgb_test(pins):
    for i in pins:
        print(i)
        GPIO.output(pins[i], GPIO.LOW)
        time.sleep(2)
        GPIO.output(pins[i], GPIO.HIGH)


