# Weather forecast application using the rpi_weather_hw and visual_crossing classes

import time
import signal

import constants
from rpi_weather_hw import RpiWeatherHW
from led8x8icons import LED8x8ICONS as ICONS

display: RpiWeatherHW

def termination_clean_up(signum, frame):
    print("Program has been quit by Ctrl-C. Cleaning Up...")
    display.hw_off()
    exit(0)

if __name__ == "__main__":
    # Initialise the HW and get a handle to it
    display = RpiWeatherHW()

    # Track termination via Ctrl+C so we can clean up
    signal.signal(signal.SIGINT, termination_clean_up)

    # Display Start-Up Behaviour
    display.scrollText(constants.weatherVer + constants.weatherCopyright, delay=0.015)
    time.sleep(1)


    # Shut down
    signal.raise_signal(signal.SIGINT)

