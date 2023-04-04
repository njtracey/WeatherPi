#===============================================================================
# clock.py
#
# Simple clock demo.
#
# 2014-09-12
# Carter Nelson
#===============================================================================
import time
import signal
import sys
import threading

import state

from led8x8icons import LED8x8ICONS as ICONS

class Clock():
    
    def __init__(self, display ):
        state.interruptAction = False
        self.display = display
        self.old_val = 8888
        self.new_val = 9999
        self.displayClockThread = None

    def time2int(self, time_struct, format24=False):
        """Convert time, passed in as a time.struct_time object, to an integer with
        hours in the hundreds place and minutes in the units place. Returns 24
        hour format if format24 is True, 12 hour format (default) otherwise.
        """
        if not isinstance(time_struct, time.struct_time):
            return None
        h = time_struct.tm_hour
        m = time_struct.tm_min
        if not format24:
            h = h if h <= 12 else h - 12
        return h*100+m

    def update_display(self, new_val, old_val, scroll=True, initial=True):
        """Update the display, one digit at a time, where values differ."""
        if not (isinstance(new_val, int) and isinstance(old_val, int)):
            return
        if new_val == old_val:
            return
        for i in range(3,-1,-1):
            new_d = new_val % 10
            old_d = old_val % 10
            if i == 0 and new_d == 0:
                # removes zero padding
                # display.scroll_raw64(ICONS['ALL_OFF'], i)
                pass
            if scroll:
                if (new_d != old_d) or initial:
                    # As we are scrolling the display, we only want to update new digits
                    # unless its the initial call to update the display
                    self.display.scroll_raw64(ICONS['{0}'.format(new_d)], i)
            else:
                # We are not scrolling on so we can just display the character
                self.display.set_raw64(ICONS['{0}'.format(new_d)], i)
            new_val = int(new_val / 10)
            old_val = int(old_val / 10)

    def threadedDisplayClock(self, initial):
        # Indicate that we shouldn't interrupt the threaded operation
        state.interruptAction = False
        # Create and start the thread to do the clock display
        self.displayClockThread = threading.Thread(
                target=self.displayClock,
                args=(initial,),
                daemon=True)
        self.displayClockThread.start()

    def threadedDisplayClockWait(self):
        # Wait for the thread to terminate
        self.displayClockThread.join()
        self.displayClockThread = None

    def turnOnClockLEDs(self):
        self.display.led_on(2)
        self.display.clock_led_on()

    def turnOffClockLEDs(self):
        self.display.led_off(2)
        self.display.clock_led_off()

    def displayClock(self,initial):
        self.old_val = 8888
        self.new_val = self.time2int(time.localtime(),True)
        self.display.led_on(2)
        self.display.clock_led_on()
        if initial:
            # Turn on all LEDs and Displays
            for m in self.display.matrix:
                m.fill(1)
                m.show()
            self.update_display(self.new_val, self.old_val, scroll=True, initial=True)
        else:
            self.update_display(self.new_val, self.old_val, scroll=False, initial=True)
        
        self.old_val = self.new_val

        while True:
            # Loop forever, updating every 2 seconds, until interruptHWAction is true.
            if state.interruptAction:
                state.interruptAction = False
                break

            self.new_val = self.time2int(time.localtime(),True)
            self.update_display(self.new_val, self.old_val, scroll=True, initial=False)
            self.display.clock_led_toggle()
            self.old_val = self.new_val
            time.sleep(2)
