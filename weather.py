# Weather forecast application using the rpi_weather_hw and visual_crossing classes

# System Imports
import time
import signal

# Project Imports
import state
import visual_crossing_apikey
import clock
from visual_crossing import VisualCrossing
from rpi_weather_hw import RpiWeatherHW
from led8x8icons import LED8x8ICONS as ICONS

# Hardware interface
display: RpiWeatherHW
# Mode classes
clock : clock.Clock

# Weather API class
theWeather : VisualCrossing

# Mode Statemachine Variables
mainMode = 0
maxMode = 3
modeTime = [10, 10, 30, 10]
cycleModes = True
firstClock = True

def mainWeatherStationEventLoop():
    global mainMode
    global maxMode
    global modeTime
    global cycleModes
    global firstClock
    global clock
    global theWeather
    global display

    while True:
        # Clock Mode
        if mainMode == 0:
            print("Entering Clock Mode...")
            clock.threadedDisplayClock(firstClock)
            firstClock = False

            # If cycling modes then switch out of mode after delay, otherwise stay in mode
            if cycleModes:
                time.sleep(modeTime[mainMode])
                # We want to move out of this mode, so terminate the clock mode thread
                state.interruptAction = True
                clock.threadedDisplayClockWait()

                # Move to next mode
                if mainMode == maxMode:
                    # Return to the mainMode 0 to cycle back through
                    mainMode = 0
                else:
                    mainMode += 1
            else:
                while True:
                    time.sleep(1)

            clock.turnOffClockLEDs()

        # Display Current Temperature
        elif mainMode == 1:
            print("Entering Current Weather Mode...")

            # Turn on the Current Temperature Mode led
            display.led_on(3)

            # Get the Mutex to avoid corrupting the weather state
            theWeather.weatherMutex.acquire()
            temperature = theWeather.currentWeatherData.temp
            theWeather.weatherMutex.release()

            tempFloat = float(temperature)
            if tempFloat < 10.0:
                tempStr = str(tempFloat)[:3]
            else:
                tempStr = str(round(tempFloat))

            # Construct the temperature string
            curTempStr = ""
            if tempFloat < 0:
                curTempStr + "-"
            curTempStr = f"{curTempStr}{tempStr}£"
            print(curTempStr)
            display.displayText(curTempStr)

            if cycleModes:
                time.sleep(modeTime[mainMode])
                if mainMode == maxMode:
                    # Return to the mainMode 0 to cycle back through
                    mainMode = 0
                else:
                    mainMode += 1
            else:
                while True:
                    time.sleep(1)

            # Turn off the Current Temperature Mode led
            display.led_off(3)

        # Display Today's Forecast Text
        elif mainMode == 2:
            print("Entering Today Forecast Weather Mode...")

            # Turn on the Current Temperature Mode led
            display.led_on(4)
            display.clear_disp()
            
            # Get the Mutex to avoid corrupting the weather state
            theWeather.weatherMutex.acquire()
            forecastDescription = theWeather.dailyWeatherData[0].description
            theWeather.weatherMutex.release()

            print("Today's forecast... " + forecastDescription)
            display.threadedScrollText("Today's forecast... " + forecastDescription)

            if cycleModes:
                time.sleep(modeTime[mainMode])
                # We want to move out of this mode, so terminate the today's forecast mode thread
                state.interruptAction = True
                display.threadedScrollTextWait()

                if mainMode == maxMode:
                    # Return to the mainMode 0 to cycle back through
                    mainMode = 0
                else:
                    mainMode += 1
            else:
                while True:
                    time.sleep(1)
                    
            # Turn on the Current Temperature Mode led
            display.led_off(4)

        # Display Next Four Days as Icons 
        elif mainMode == 3:
            print("Entering Four Day Forecast Weather Mode...")

            # Turn on the Current Temperature Mode led
            display.led_on(5)
            

            # Get the Mutex to avoid corrupting the weather state
            theWeather.weatherMutex.acquire()
            icon0 = theWeather.dailyWeatherData[0].icon
            icon1 = theWeather.dailyWeatherData[1].icon
            icon2 = theWeather.dailyWeatherData[2].icon
            icon3 = theWeather.dailyWeatherData[3].icon
            theWeather.weatherMutex.release()

            display.displayIcons(icon0, icon1, icon2, icon3)
            print(f"{icon0}, {icon1}, {icon2}, {icon3}")

            if cycleModes:
                time.sleep(modeTime[mainMode])
                if mainMode == maxMode:
                    # Return to the mainMode 0 to cycle back through
                    mainMode = 0
                else:
                    mainMode += 1
            else:
                while True:
                    time.sleep(1)
                    
            # Turn on the Current Temperature Mode led
            display.led_off(5)

        time.sleep(0.1)

def termination_clean_up(signum, frame):
    print("Program has been quit by Ctrl-C. Cleaning Up...")
    display.hw_off()
    exit(0)

if __name__ == "__main__":
    # Initialise the HW and get a handle to it
    display = RpiWeatherHW()

    # Initialise the Mode Classes
    clock = clock.Clock(display)

    # Track termination via Ctrl+C so we can clean up
    signal.signal(signal.SIGINT, termination_clean_up)

    # Initiate the Weather API to get weather data
    theWeather = VisualCrossing(visual_crossing_apikey.myVisualCrossingAPIKey)
    theWeather.setLocation("Liverpool", "53.39079,-2.9055259")
    theWeather.addSublocations("York", "53.9270239,-1.0741348")
    theWeather.addSublocations("London", "51.4892971,-0.1132849")
    theWeather.setPollingPeriod(60)
    theWeather.pollForWeatherWithThread()

    # Display Start-Up Behaviour
    display.threadedScrollText(state.weatherVer + state.weatherCopyright, delay=0.005)
    time.sleep(1)
    state.interruptAction = True
    display.threadedScrollTextWait()

    # Enter the main state-machine loop for the Weather Station
    mainMode = 0
    mainWeatherStationEventLoop()

    # Shut down
    signal.raise_signal(signal.SIGINT)

