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
* ```clock_test.py``` - displays the time, for use as a clock as a test app for the displays and HW
* ```clock.py``` - contains a class for managing the clock mode of the weather station functionality
* ```weather.py``` - the main application contianing the state-machine to drive the modes of the weather station
* ```visual_crossing.py``` - interfaces the VisualCrossing Web API to download weather data
* ```visual_crossing_apikey.py``` - put your VisualCrossing API key here... myVisualCrossingAPIKey=\<Your Key Here\>

# Modes of Operation
The weather station has various modes, which are indicated by the six red LEDs, numbered from 0 to 5 from top-left, to
bottom-left, then top-right to bottom-right. The modes are:
1. Mode 0: Clock - displays the current time
1. Mode 1: Current Temperature - displays the current temperature at the current location
1. Mode 2: Rainfull - displays the probability and amount of rain today
1. Mode 3: Next Four Hours - displays icons for the weather in the next four hours
1. Mode 4: Next Four Days - displays icons for the weather in the next four days
1. Mode 5: Bin Recycling - displays the day and type of the next bin recycling

In addition via the buttons its possible to access:
* A detailed weather forecast in textual form for the rest of the day and the four day forecasting period
* The weather details for the sub location

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

