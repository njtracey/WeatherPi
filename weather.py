# Weather forecast application using the rpi_weather_hw and visual_crossing classes

# System Imports
import time
import signal
import datetime

# Project Imports
import state
import visual_crossing_apikey
import clock
import weather_modes
import sounds
import rubbish
from visual_crossing import VisualCrossing
from rpi_weather_hw import RpiWeatherHW
from led8x8icons import LED8x8ICONS as ICONS

# Hardware interface
display: RpiWeatherHW
# Mode classes
clock : clock.Clock
weather : weather_modes.WeatherDisplay

# Weather API class
theWeather : VisualCrossing

# Mode Statemachine Variables
mainMode = 0
oldMainMode = 0
maxMode = 5
modeTime = [10, 10, 9, 10, 10, 10]
cycleModes = True
firstClock = True

def extractWeatherForecastText(theWeather,short=False,subLocationName=""):
    
    # Get the Mutex to avoid corrupting the weather state
    theWeather.weatherMutex.acquire()
    if short:
        todaysDescription = theWeather.currentSubWeatherData[subLocationName].conditions
        todaysTemp = theWeather.currentSubWeatherData[subLocationName].temp
        todaysTempFeelsLike = theWeather.currentSubWeatherData[subLocationName].feelslike
    else:
        todayDescription = theWeather.dailyWeatherData[0].description
        todayTempMin = theWeather.dailyWeatherData[0].tempmin
        todayTempMax = theWeather.dailyWeatherData[0].tempmax
        todayTempFeelsLike = theWeather.dailyWeatherData[0].feelslike
        todayPrecip = theWeather.dailyWeatherData[0].precip
        todayPrecipType = theWeather.dailyWeatherData[0].preciptype
        todayPrecipProb = int(theWeather.dailyWeatherData[0].precipprob)
    theWeather.weatherMutex.release()

    if short:
        forecastString = "Conditions in " + subLocationName + " today, " + str(todaysDescription)
        forecastString = forecastString + ". With a temperature of " + str(todaysTemp) + "£" + \
                " and feeling like " + str(todaysTempFeelsLike) + "£.    "
    else:
        forecastString = "Today the weather will be " + todayDescription
        forecastString = forecastString + " The high will be " + str(todayTempMax) + "£" + \
            " and the low will be " + str(todayTempMin) + "£."
        forecastString = forecastString + " There is a " + str(todayPrecipProb) + "% chance of"
        precipTypeNum = 0
        for p in todayPrecipType:
            if p == 'rain':
                if precipTypeNum != 0:
                    forecastString = forecastString + " &"
                    forecastString = forecastString + " rain"
                    precipTypeNum += 1
            if p == 'snow':
                if precipTypeNum != 0:
                    forecastString = forecastString + " &"
                    forecastString = forecastString + " snow"
                    precipTypeNum += 1

        if precipTypeNum == 0:
            forecastString = forecastString + " rain"

        forecastString = forecastString + " with a depth of " + str(todayPrecip) + "mm."
        forecastString = forecastString + "    "

    return forecastString

def mainWeatherStationEventLoop():
    global mainMode
    global oldMainMode
    global maxMode
    global modeTime
    global cycleModes
    global firstClock
    global clock
    global theWeather
    global display

    while True:
        # Main state machine for weather station, driving the modal behaviour
        # Mode 0: Clock
        # Mode 1: Current Temperature
        # Mode 2: Today's Precipitation
        # Mode 3: Next Four Hours
        # Mode 4: New Four Days
        # Mode 5: Bin Recycling

        # Clock Mode
        if mainMode == 0:
            print("Entering Clock Mode...")

            # Turn off the Rubbish Mode led
            display.led_off(7)

            display.clear_disp()
            clock.turnOnClockLEDs()

            state.interruptAction = False
            clock.threadedDisplayClock(firstClock)
            firstClock = False

            # If cycling modes then switch out of mode after delay, otherwise stay in mode
            if cycleModes:
                # Cycling mode, so stay in this mode until modeTime expires unless interrupted
                for i in range(modeTime[mainMode]*10):
                    if state.interruptAction:
                        break
                    time.sleep(0.1)

                if state.interruptAction == False:
                    # We want to move out of this mode, so terminate the clock mode thread
                    state.interruptAction = True
                    clock.threadedDisplayClockWait()
                    state.interruptAction = False

                    # Move to next mode
                    if mainMode >= maxMode:
                        # Return to the mainMode 0 to cycle back through
                        mainMode = 0
                    else:
                        mainMode += 1
                else:
                    clock.threadedDisplayClockWait()
                    state.interruptAction = False
            else:
                while True:
                    if state.interruptAction:
                        clock.threadedDisplayClockWait()
                        state.interruptAction = False
                        break
                    time.sleep(0.1)

        # Display Current Temperature
        elif mainMode == 1:
            print("Entering Current Temperature Mode...")

            # Turn off the Clock Mode leds
            clock.turnOffClockLEDs()
            # Turn on the Current Temperature Mode led
            display.led_on(3)

            if theWeather.weatherDataAvailable:
                weather.threadedDisplayTemperature()
            else:
                weather.threadedDisplayError()

            if cycleModes:
                # Cycling mode, so stay in this mode until modeTime expires unless interrupted
                for i in range(modeTime[mainMode]*10):
                    if state.interruptAction:
                        break
                    time.sleep(0.1)

                if state.interruptAction == False:
                    # We want to move out of this mode, so terminate the weather mode thread
                    state.interruptAction = True
                    weather.threadedDisplayTemperatureWait()
                    state.interruptAction = False

                    #Move to next mode
                    if mainMode >= maxMode:
                        # Return to the mainMode 0 to cycle back through
                        mainMode = 0
                    else:
                        mainMode += 1
                else:
                    weather.threadedDisplayTemperatureWait()
                    state.interruptAction = False
            else:
                while True:
                    if state.interruptAction:
                        weather.threadedDisplayTemperatureWait()
                        state.interruptAction = False
                        break
                    time.sleep(0.1)

        # Display Today's Rain Fall 
        elif mainMode == 2:
            print("Entering Current Precipitation Mode...")

            # Turn off the Current Temperature Mode led
            display.led_off(3)
            # Turn on the Precipitation Mode led
            display.clear_disp()
            display.led_on(4)

            if theWeather.weatherDataAvailable:
                weather.threadedDisplayPrecipitation()
            else:
                weather.threadedDisplayError()

            if cycleModes:
                # Cycling mode, so stay in this mode until modeTime expires unless interrupted
                for i in range(modeTime[mainMode]*10):
                    if state.interruptAction:
                        break
                    time.sleep(0.1)

                if state.interruptAction == False:
                    # We want to move out of this mode, so terminate the weather mode thread
                    state.interruptAction = True
                    weather.threadedDisplayPrecipitationWait()
                    state.interruptAction = False

                    # Move to next mode
                    if mainMode >= maxMode:
                        # Return to the mainMode 0 to cycle back through
                        mainMode = 0
                    else:
                        mainMode += 1
                else:
                    weather.threadedDisplayPrecipitationWait()
                    state.interruptAction = False
            else:
                while True:
                    if state.interruptAction:
                        weather.threadedDisplayPrecipitationWait()
                        state.interruptAction = False
                        break
                    time.sleep(0.1)

        # Display Next Four Hours as Icons 
        elif mainMode == 3:
            print("Entering Four Hour Forecast Weather Mode...")

            # Turn off the Precipitation Mode led
            display.led_off(4)
            # Turn on the Current Temperature Mode led
            display.led_on(5)
            
            if theWeather.weatherDataAvailable:
                # Get the Mutex to avoid corrupting the weather state
                theWeather.weatherMutex.acquire()

                # Find the starting hourly forecast
                hourIconsFound = 0
                hourIcons = []

                hourlyStartIndex = 0
                currentTimeEpoch = time.time()
                for h in theWeather.dailyWeatherData[0].hourly:
                    if h.timeepoc >= currentTimeEpoch:
                        break
                    hourlyStartIndex += 1
                if hourlyStartIndex >= 24:
                    for i in range(4):
                        hourIcons.append(theWeather.dailyWeatherData[1].hourly[i].icon)
                else:
                    for i in range(4):
                        index = i + hourlyStartIndex
                        dayWrap = False
                        if index > 23:
                            index = index - 23
                            dayWrap = True
                        if dayWrap:
                            hourIcons.append(theWeather.dailyWeatherData[0].hourly[index].icon)
                        else:
                            hourIcons.append(theWeather.dailyWeatherData[1].hourly[index].icon)
                theWeather.weatherMutex.release()

                display.displayIcons(hourIcons[0], hourIcons[1], hourIcons[2], hourIcons[3])
            else:
                display.displayError()

            if cycleModes:
                # Cycling mode, so stay in this mode until modeTime expires unless interrupted
                for i in range(modeTime[mainMode]*10):
                    if state.interruptAction:
                        break
                    time.sleep(0.1)

                if state.interruptAction == False:
                    if mainMode >= maxMode:
                        # Return to the mainMode 0 to cycle back through
                        mainMode = 0
                    else:
                        mainMode += 1
                else:
                    state.interruptAction = False

        # Display Next Four Days as Icons 
        elif mainMode == 4:
            print("Entering Four Day Forecast Weather Mode...")

            # Turn off the Four Hour Mode led
            display.led_off(5)
            # Turn on the Four Day Mode led
            display.led_on(6)
            
            if theWeather.weatherDataAvailable:
                # Get the Mutex to avoid corrupting the weather state
                theWeather.weatherMutex.acquire()
                icon0 = theWeather.dailyWeatherData[0].icon
                icon1 = theWeather.dailyWeatherData[1].icon
                icon2 = theWeather.dailyWeatherData[2].icon
                icon3 = theWeather.dailyWeatherData[3].icon
                theWeather.weatherMutex.release()

                display.displayIcons(icon0, icon1, icon2, icon3)
            else:
                display.displayError()

            if cycleModes:
                # Cycling mode, so stay in this mode until modeTime expires unless interrupted
                for i in range(modeTime[mainMode]*10):
                    if state.interruptAction:
                        break
                    time.sleep(0.1)

                if state.interruptAction == False:
                    if mainMode >= maxMode:
                        # Return to the mainMode 0 to cycle back through
                        mainMode = 0
                    else:
                        mainMode += 1
                else:
                    state.interruptAction = False
                    
        elif mainMode == 5:
            print("Entering Rubbish Collection Mode...")

            # Turn off the Four Day Mode led
            display.led_off(6)
            # Turn on the Rubbish Mode led
            display.led_on(7)

            today = datetime.date.today()
            for r in rubbish.rubbishCollectionCalendar:
                if datetime.date.fromisoformat(r) >= today:
                    rubbishKey = r
                    break
            rubbishDate = datetime.date.fromisoformat(rubbishKey)

            if rubbishDate.weekday() == 0:
                display.displayText("Mon")
            elif rubbishDate.weekday() == 1:
                display.displayText("Tue")
            elif rubbishDate.weekday() == 2:
                display.displayText("Wed")
            elif rubbishDate.weekday() == 3:
                display.displayText("Thu")
            elif rubbishDate.weekday() == 4:
                display.displayText("Fri")
            elif rubbishDate.weekday() == 5:
                display.displayText("Sat")
            elif rubbishDate.weekday() == 6:
                display.displayText("Sun")
            else:
                pass

            display.set_raw64(ICONS[rubbish.rubbishCollectionCalendar[rubbishKey]], matrix=3)

            if cycleModes:
                # Cycling mode, so stay in this mode until modeTime expires unless interrupted
                for i in range(modeTime[mainMode]*10):
                    if state.interruptAction:
                        break
                    time.sleep(0.1)

                if state.interruptAction == False:
                    if mainMode >= maxMode:
                        # Return to the mainMode 0 to cycle back through
                        mainMode = 0
                    else:
                        mainMode += 1
                else:
                    state.interruptAction = False
                    
        # Display Forecast Text
        elif mainMode == 6:
            print("Entering Forecast Description Weather Mode...")

            state.interruptAction = False

            # Turn on the Current Temperature Mode led
            display.all_led_off()
            display.clear_disp()

            if theWeather.weatherDataAvailable:
                forecastString = extractWeatherForecastText(theWeather)
            
                soundPlayer.threadedPlayText(forecastString.replace('£', ' degrees'))
                display.scrollText(forecastString, delay=0.01)
            else:
                display.displayError()

            # Special handling to allow entry to sound mode when holding button 2
            if mainMode == 8:
                # Button must have been held to switch to mode 8 by continuing outer loop and configure sound
                continue

            mainMode = oldMainMode
            if mainMode >= maxMode:
                # Return to the mainMode 0 to cycle back through
                mainMode = 0

        # Display Sublocation Forecast Text
        elif mainMode == 7:
            print("Entering Forecast for Sublocation Mode...")

            state.interruptAction = False

            # Turn on the Current Temperature Mode led
            display.all_led_off()
            display.clear_disp()

            if theWeather.weatherDataAvailable:
                for subLoc in theWeather.subLocations:
                    if state.interruptAction:
                        break

                    forecastString = extractWeatherForecastText(theWeather,short=True,subLocationName=subLoc)
            
                    soundPlayer.threadedPlayText(forecastString.replace('£', ' degrees'))
                    display.scrollText(forecastString, delay=0.01)
            else:
                display.displayError()

            mainMode = oldMainMode
            if mainMode >= maxMode:
                # Return to the mainMode 0 to cycle back through
                mainMode = 0

        # Display Sound Toggle Mode
        elif mainMode == 8:
            print("Entering Sound Toggle Mode...")

            state.interruptAction = False

            # Turn on the Current Temperature Mode led
            display.all_led_off()
            display.clear_disp()

            # Toggle sound state
            state.soundsOn = not state.soundsOn

            soundStateString = "Sound:"
            if state.soundsOn:
                soundStateString = soundStateString + "On    "
            else:
                soundStateString = soundStateString + "Off    "

            display.scrollText(soundStateString, delay=0.01)

            state.interruptAction = False

            mainMode = oldMainMode
            if mainMode >= maxMode:
                # Return to the mainMode 0 to cycle back through
                mainMode = 0

        time.sleep(0.1)

def termination_clean_up(signum, frame):
    global theWeather

    print("Program has been quit by Ctrl-C. Cleaning Up...")
    state.interruptAction = True
    theWeather.stopPollingForWeather()
    display.hw_off()
    print("Program has been quit by Ctrl-C. Cleaning Up Finished. Goodbye!")
    exit(0)

def button0Pressed():
    global cycleModes
    global mainMode
    global display

    cycleModes = False
    if mainMode >= maxMode:
        # Return to the mainMode 0 to cycle back through
        mainMode = 0
    else:
        mainMode += 1
    state.interruptAction = True

def button0Held():
    global cycleModes
    global mainMode
    global display

    cycleModes = True
    mainMode = 0
    display.all_led_off()
    display.clear_disp()
    state.interruptAction = True

def button1Pressed():
    global cycleModes
    global mainMode

def button2Pressed():
    global cycleModes
    global mainMode
    global oldMainMode

    oldMainMode = mainMode
    mainMode = 6
    state.interruptAction = True

def button2Held():
    global cycleModes
    global mainMode
    global display

    oldMainMode = mainMode
    mainMode = 8
    state.interruptAction = True
    state.switchToMode8 = True

def button3Pressed():
    global cycleModes
    global mainMode
    global oldMainMode

    oldMainMode = mainMode
    mainMode = 7
    state.interruptAction = True

if __name__ == "__main__":
    # Track termination via Ctrl+C so we can clean up
    signal.signal(signal.SIGINT, termination_clean_up)

    # Initialise the HW and get a handle to it
    display = RpiWeatherHW()

    # Configure the button interrupts and map them to their function calls
    RpiWeatherHW.buttons[0].when_pressed = button0Pressed
    RpiWeatherHW.buttons[0].when_held = button0Held
    RpiWeatherHW.buttons[1].when_pressed = button1Pressed
    RpiWeatherHW.buttons[2].when_pressed = button2Pressed
    RpiWeatherHW.buttons[2].when_held = button2Held
    RpiWeatherHW.buttons[3].when_pressed = button3Pressed

    # Initiate the Weather API to get weather data
    theWeather = VisualCrossing(visual_crossing_apikey.myVisualCrossingAPIKey)
    theWeather.setLocation("Liverpool", "53.39079,-2.9055259")
    theWeather.addSublocations("York", "53.9270239,-1.0741348")
    theWeather.addSublocations("London", "51.4892971,-0.1132849")
    theWeather.setPollingPeriod(120)
    theWeather.pollForWeatherWithThread()

    # Initialise the Mode Classes
    soundPlayer = sounds.SoundPlayer()
    clock = clock.Clock(display, soundPlayer)
    weather = weather_modes.WeatherDisplay(display, theWeather)

    # Display Start-Up Behaviour
    display.scrollText(state.weatherVer + state.weatherCopyright, delay=0.005)

    # Enter the main state-machine loop for the Weather Station
    mainMode = 0
    mainWeatherStationEventLoop()
    # Above event loop should never terminate

    # Shut down
    signal.raise_signal(signal.SIGINT)

