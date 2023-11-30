
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
    auto_write=True,
    pixel_order=ORDER
)

# Alle LED schwarz
pixels.fill((0,0,0))
