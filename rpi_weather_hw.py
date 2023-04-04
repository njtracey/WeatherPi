#===============================================================================
# Class for abstracting the HW set up which consists of four Adafruit 8x8
# matrix displays attached to i2c, 8 leds and four bittons
#
# (c) GrumpyFerret - Nigel Tracey
#===============================================================================

from time import sleep
from gpiozero import LED
import board
import busio
import threading
from adafruit_ht16k33 import matrix

import state
from led8x8icons import LED8x8ICONS as ICONS

class RpiWeatherHW():

    # Hardware interface variables
    leds = [LED(17), LED(27), LED(22), LED(10), LED(9), LED(14), LED(15), LED(18)]

    # State of Clock LEDs - True=On; False=Off
    clock_leds = False

    def __init__(self, ):
        i2c = busio.I2C(board.SCL, board.SDA)
        RpiWeatherHW.matrix = []
        RpiWeatherHW.matrix.append(matrix.Matrix8x8(i2c, address=0x70))
        RpiWeatherHW.matrix.append(matrix.Matrix8x8(i2c, address=0x71))
        RpiWeatherHW.matrix.append(matrix.Matrix8x8(i2c, address=0x72))
        RpiWeatherHW.matrix.append(matrix.Matrix8x8(i2c, address=0x73))
        # Turn on all LEDs and Displays
        for m in RpiWeatherHW.matrix:
            m.fill(1)
        for led in RpiWeatherHW.leds:
            led.on()
        sleep(2)

        # Turn off all LEDs and Displays
        for m in RpiWeatherHW.matrix:
            m.fill(0)
        for led in RpiWeatherHW.leds:
            led.off()

        """ Turn off auto display update """
        for m in RpiWeatherHW.matrix:
            m.auto_write = False

        state.interruptAction = False
        RpiWeatherHW.displayUpdateThread = None

    def hw_off(self):
        for led in RpiWeatherHW.leds:
            led.off()
        for m in RpiWeatherHW.matrix:
            m.fill(0)
            m.show()
            
    def clock_led_toggle(self):
        if RpiWeatherHW.clock_leds:
           RpiWeatherHW.leds[0].off()
           RpiWeatherHW.leds[1].off()
           RpiWeatherHW.clock_leds = False
        else:
           RpiWeatherHW.leds[0].on()
           RpiWeatherHW.leds[1].on()
           RpiWeatherHW.clock_leds = True
   
    def clock_led_on(self):
       RpiWeatherHW.leds[0].on()
       RpiWeatherHW.leds[1].on()
       RpiWeatherHW.clock_leds = True
   
    def clock_led_off(self):
       RpiWeatherHW.leds[0].off()
       RpiWeatherHW.leds[1].off()
       RpiWeatherHW.clock_leds = False

    def all_led_on(self):
        for l in RpiWeatherHW.leds:
            l.on()

    def all_led_off(self):
        for l in RpiWeatherHW.leds:
            l.off()

    def led_on(self, ledNumber):
        if 0 <= ledNumber < len(RpiWeatherHW.leds): 
            RpiWeatherHW.leds[ledNumber].on()

    def led_off(self, ledNumber):
        if 0 <= ledNumber < len(RpiWeatherHW.leds): 
            RpiWeatherHW.leds[ledNumber].off()
   
    def is_valid_matrix(self, matrix):
        """Returns True if matrix number is valid, otherwise False."""
        return matrix in range(len(RpiWeatherHW.matrix))     
          
    def clear_disp(self, matrix=None):
        """Clear specified matrix. If none specified, clear all."""
        if matrix == None:
            for m in RpiWeatherHW.matrix:
                m.fill(0)
                m.show()
        else:
            if not self.is_valid_matrix(matrix):
                return
            RpiWeatherHW.matrix[matrix].fill(0)
            RpiWeatherHW.matrix[matrix].show()
            
    def set_pixel(self, x, y, matrix=0, value=1):
        """Set pixel at position x, y for specified matrix to the given value."""
        if not self.is_valid_matrix(matrix):
            return
        RpiWeatherHW.matrix[matrix][x, y] = value
        RpiWeatherHW.matrix[matrix].show()
          
    def set_bitmap(self, bitmap, matrix=0):
        """Set specified matrix to provided bitmap."""
        if not self.is_valid_matrix(matrix):
            return
        for x in range(8):
            for y in range(8):
                RpiWeatherHW.matrix[matrix][x, y] = bitmap[y][x]
        RpiWeatherHW.matrix[matrix].show()
        
    def set_raw64(self, value, matrix=0):
        """Set specified matrix to bitmap defined by 64 bit value."""
        if not self.is_valid_matrix(matrix):
            return
        RpiWeatherHW.matrix[matrix].fill(0)
        for y in range(8):
            row_byte = value >> (8*y)
            for x in range(8):
                pixel_bit = row_byte >> x & 0x01
                RpiWeatherHW.matrix[matrix][x, y] = pixel_bit 
        RpiWeatherHW.matrix[matrix].show()
        
    def scroll_raw64(self, value, matrix=0, delay=0.15):
        """Scroll out the current bitmap with the supplied bitmap. Can also
        specify a matrix (0-3) and a delay to set scroll rate.
        """
        for step in range(7,-1,-1):
            RpiWeatherHW.matrix[matrix].shift_up()
            row_byte = value >> (8*step)
            for x in range(8):
                pixel_bit = row_byte >> x & 0x01
                RpiWeatherHW.matrix[matrix][x,0] = pixel_bit
            RpiWeatherHW.matrix[matrix].show()
            sleep(delay)

    def displayText(self, text):
        if len(text) > 4:
            displayText = text[:4]
        else:
            displayText = text

        for i, c in enumerate(displayText):
            self.set_raw64(ICONS[c], matrix=i)

    def displayIcons(self, icon0, icon1, icon2, icon3):
        self.set_raw64(ICONS[icon0], 0)
        self.set_raw64(ICONS[icon1], 1)
        self.set_raw64(ICONS[icon2], 2)
        self.set_raw64(ICONS[icon3], 3)

    def interruptDisplayAction(self):
        # Set the flag to indicate that scrolling should be interrupted
        state.interruptAction = True

    def threadedScrollText(self, text_message, delay=0.03):
        # Indicate that we shouldn't interrupt the threaded operation
        state.interruptAction = False
        # Create and start the thread to do the scrolling
        RpiWeatherHW.displayUpdateThread = threading.Thread(
                target=self.scrollText,
                args=(text_message, delay),
                daemon=True)
        RpiWeatherHW.displayUpdateThread.start()

    def threadedScrollTextWait(self):
        # Wait for the thread to terminate
        RpiWeatherHW.displayUpdateThread.join()
        RpiWeatherHW.displayUpdateThread = None

    def scrollText(self, text_message, delay=0.03):
        bitmap = [[0 for x in range(8)] for y in range(8)]

        """Scroll a text message across all four displays"""
        for character in text_message:

            # Check if we should terminate the scrolling
            if state.interruptAction:
                # Reset the flag so it doesn't interrupt next time
                state.interruptAction = False
                return

            """ Construct the bitmap """
            value = ICONS['{0}'.format(character)]
            for y in range(8):
                row_byte = value >> (8*y)
                for x in range(8):
                    pixel_bit = row_byte >> x & 0x01
                    bitmap[x][y] = pixel_bit

            """ Scroll the text onto the display moving everything else left """
            for x in range(8):
                """ First Move the left column of each display to the right column of the next display before shifting """
                for i in range(3):
                    for y in range(8):
                        RpiWeatherHW.matrix[i][7,y] = RpiWeatherHW.matrix[i+1][0,y]

                """ Shift all displays to the left """
                for i in range(4):
                    RpiWeatherHW.matrix[i].shift_left()

                """ Now add in the new stripe of text for the current caracter """
                for y in range(8):
                    RpiWeatherHW.matrix[3][7,y] = bitmap[x][y]

                """ Show the results """
                for i in range(4):
                    RpiWeatherHW.matrix[i].show()
                sleep(delay)
                
    def disp_number(self, number):
        """Display number as integer. Valid range is 0 to 9999."""
        num = int(number)
        if num > 9999 or num < 0:
            return
        self.clear_disp()
        matrix = 3
        while num:
            digit = num % 10
            self.set_raw64(ICONS['{0}'.format(digit)], matrix)
            num = int(num / 10)
            matrix -= 1

