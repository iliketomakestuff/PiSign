#!/usr/bin/python

# This is assuming you've followed the instructions at
# https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices

# A more complex RGBMatrix example works with the Python Imaging Library,
# demonstrating a few graphics primitives and image loading.
# Note that PIL graphics do not have an immediate effect on the display --
# image is drawn into a separate buffer, which is then copied to the matrix
# using the SetImage() function (see examples below).
# Requires rgbmatrix.so present in the same directory.

# PIL Image module (create or load images) is explained here:
# http://effbot.org/imagingbook/image.htm
# PIL ImageDraw module (draw shapes to images) explained here:
# http://effbot.org/imagingbook/imagedraw.htm

# This project was created by Bob Clagett of I Like To Make Stuff
# More details and build video available at http://www.iliketomakestuff.com/

import Image
import ImageDraw
import time
import os
from rgbmatrix import Adafruit_RGBmatrix

import RPi.GPIO as GPIO

imagePath = '/home/pi/rpi-rgb-led-matrix-master/'
pressed = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# on/off button
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(14, GPIO.OUT)  # led
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button

GPIO.setup(15, GPIO.OUT)  # led
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button

GPIO.setup(25, GPIO.OUT)  # led
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button

GPIO.setup(19, GPIO.OUT)  # led
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 1)
matrix.SetWriteCycles(4)
# Bitmap example w/graphics prims
image = Image.new("1", (32, 32))  # Can be larger than matrix if wanted!!

leds = {
    18: 14,
    24: 15,
    8: 25,
    7: 19
}


def showReady():
    lp = 0
    # runs a simple animation with the buttons LEDS so you know it's ready.
    while lp < 5:
        for key in leds:
            GPIO.output(leds[key], True)
            time.sleep(.15)
            GPIO.output(leds[key], False)
        lp += 1
    image = Image.open(imagePath + "logo.jpg")
    image.load()
    matrix.SetImage(image.im.id, 0, 1)
    time.sleep(2)
    matrix.Clear()


def clearlights():
    for key in leds:
        GPIO.output(leds[key], False)


def lookForButtons(buttonNum):
    global pressed
    input_state = GPIO.input(buttonNum)
    if input_state == False:
        clearlights()
        # print('press '+str(buttonNum))
        if buttonNum != pressed:
            # new button was pressed
            GPIO.output(leds.get(buttonNum, ''), True)
            pictures = {
                18: 'danger.gif',
                8: 'onair.gif',
                24: 'filming.gif',
                7: 'logo2.jpg'
            }
            time.sleep(0.2)
            image = Image.open(imagePath + pictures.get(buttonNum, ''))
            image.load()
            matrix.SetImage(image.im.id, 0, 1)
            pressed = buttonNum

        else:
            # active button was re-pressed, turn it off and clear screen
            matrix.Clear()
            matrix.Fill(0x000000)

            pressed = 0

            time.sleep(.6)


def lookForShutDown():
    shutDownButton = GPIO.input(3)
    if shutDownButton == False:
        showReady()
        os.system('shutdown now -h')


# setup complete, start running stuff
matrix.Clear()
print('PiSign loaded.....  rock on    \m/')
showReady()

while True:
    lookForButtons(18)
    lookForButtons(24)
    lookForButtons(8)
    lookForButtons(7)
    lookForShutDown()
