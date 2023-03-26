# Raspberry Pi Weather Station
Python 3 application for a Raspberry Pi to download weather via the VisualCrossing API and display it on
the Adafruit 8x8 matrix displays, 8 LEDs and 4 buttons of the dedicated HW set-up.

# Hardware
This program should work with any Raspberry Pi. It is also set-up with 4 Adafruit 8x8 LED
Matrices with I2C Backpacks that have the  address jumpers to set unique addresses for each.
Expected range is 0x70-0x73. There are also 8 LEDs (6 red and 2 yellow) and 4 buttons.
Look at the file rpi-weather.fzz for the wiring diagram.

# Software
A brief description of the various software components.
* ```rpi_weather_hw.py``` - defines a class for interfacing with the hardware
* ```led8x8icons.py``` - contains a dictionary of icons
* ```clock.py``` - displays the time, for use as a clock as a test app for the displays and HW
* ```visual_crossing.py``` - interfaces the VisualCrossing Web API to download weather data
* ```visual_crossing_apikey.py``` - put your VisualCrossing API key here... myVisualCrossingAPIKey=<Your Key Here>

# Dependencies
*  Adafruit Python Library for LED Backpacks
    * https://github.com/adafruit/Adafruit_Python_LED_Backpack

# Install
Simply clone this repo and run:
```
$ git clone https://github.com/njtracey
$ cd rpi-weather
$ sudo python 
```

