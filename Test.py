# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
NeoPixel example for Pico. Turns the NeoPixels red.

REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP0.
"""
import board
import neopixel
import time
from rainbowio import colorwheel

# Update this to match the number of NeoPixel LEDs connected to your board.
# Number of pixels in this strip is 330.
num_pixels = 330

pixels = neopixel.NeoPixel(board.GP0, num_pixels, auto_write=False)
pixels.brightness = 0.6

def rainbow(speed):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(speed)
    
colour = (220, 0, 0)
zero = (0, 0, 0)
index = 50
wait = 0.4
while True:
    pixels[index] = colour
    pixels.show()
    time.sleep(wait)
    pixels[index] = zero
    pixels.show()
    time.sleep(wait)
    
    