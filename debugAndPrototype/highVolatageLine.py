import board, neopixel, time
from datetime import datetime, timedelta
import numpy as np
import random

# set up the LEDs with the Raspberry Pi
pixel_pin = board.D18
num_pixels = 102
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(
    pixel_pin, 
    num_pixels, 
    brightness=1,
    auto_write=False,
    pixel_order=ORDER
)
"""
#0 - 255
pixels.fill((0,0,0))
pixels[1] = 0,0,0
pixels.show()

BRG
"""

# Alle LED schwarz
pixels.fill((0,0,0))

index = -1
AnzahlLed = 101
"""
time.sleep(0.0006)
start = time.time()
NowTime = datetime.now()

NowSecond = NowTime.strftime('%S')
"""

def BlitzStrobo(anzahl):
    count = 0   
    while True:
        pixels.fill((255,255,255))
        pixels.show()
        time.sleep(0.01)
        pixels.fill((0,0,0))
        pixels.show()
        count = count+1
        time.sleep(0.05)

        if count == anzahl:
            count = 0
            break
 
def BlitzAbfolge():
    index = -1
    while True:
        pixels[index] = 0,0,0
        pixels[index+1] = 255,255,255
        #pixels[index+1] = 3,255,223

        index = index+1

        if index == AnzahlLed:
            index = -1
            #time.sleep(random.randint(0, 20))
            break
        pixels.show()

def RandomLed(anzahl):
    anzahl = anzahl*1000
    count = 0
    while True:
        randompixel = random.randint(0, 100)
        pixels[randompixel] = 10,10,10
        #time.sleep(0.02)
        pixels.show()

        pixels[randompixel] = 0,0,0
        count += 1
        if count == anzahl:
            break
            

while True:

    BlitzStrobo(3)
    time.sleep(2)
    BlitzAbfolge()
    #time.sleep(3)
    #time.sleep(random.randint(0, 10))
    RandomLed(1)
   
