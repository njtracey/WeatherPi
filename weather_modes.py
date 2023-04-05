# Class for handling the weather display modes

import time
import threading

import state
from led8x8icons import LED8x8ICONS as ICONS

class WeatherDisplay():

    def __init__(self, display, weatherData):
        state.interruptAction = False
        self.display = display
        self.weatherData = weatherData
        self.displayWeatherDataThread = None

    def threadedDisplayTemperature(self):
        # Indicate that we shouldn't interrupt the threaded operation
        state.interruptAction = False
        # Create and start the thread to do the current temperature display
        self.displayWeatherDataThread = threading.Thread(
                target = self.displayTemperature,
                args=(),
                daemon=True)
        self.displayWeatherDataThread.start()

    def threadedDisplayTemperatureWait(self):
        self.threadedWeatherWait()

    def threadedWeatherWait(self):
        # Wait for the thread to terminate
        self.displayWeatherDataThread.join()
        self.displayWeatherDataThread = None

    def displayTemperature(self):
        cachedWeatherTimer = 0
        firstTime = True
        while True:
            if state.interruptAction:
                break
            
            # Only update the weather data and display every 30 seconds or on first iteration
            if cachedWeatherTimer == 300 or firstTime:
                cachedWeatherTimer = 0
                firstTime = False

                # Get the weather data within the mutex to avoid corruption
                self.weatherData.weatherMutex.acquire()
                temperature = self.weatherData.currentWeatherData.temp
                self.weatherData.weatherMutex.release()

                # Construct the temperature string
                tempFloat = float(temperature)
                if tempFloat < 10.0:
                    tempStr = str(tempFloat)[:3]
                else:
                    tempStr = str(round(tempFloat))

                curTempStr = ""
                if tempFloat < 0:
                    curTempStr + "-"
                curTempStr = f"{curTempStr}{tempStr}£"
                
                # Display the temperature
                self.display.clear_disp()
                self.display.displayText(curTempStr)
            else:
                cachedWeatherTimer += 1

            time.sleep(0.1)

    def threadedDisplayPrecipitation(self):
        # Indicate that we shouldn't interrupt the threaded operation
        state.interruptAction = False
        # Create and start the thread to do the current temperature display
        self.displayWeatherDataThread = threading.Thread(
                target = self.displayPrecipitation,
                args=(),
                daemon=True)
        self.displayWeatherDataThread.start()

    def threadedDisplayPrecipitationWait(self):
        self.threadedWeatherWait()

    def displayPrecipitation(self):
        while True:
            if state.interruptAction:
                break

            # Get the Mutex to avoid corrupting the weather state
            self.weatherData.weatherMutex.acquire()
            precip = self.weatherData.dailyWeatherData[0].precip
            precipProb = self.weatherData.dailyWeatherData[0].precipprob
            precipType = self.weatherData.dailyWeatherData[0].preciptype
            self.weatherData.weatherMutex.release()

            # Display the precipitation

            rain = False
            snow = False
            for p in precipType:
                if p == "rain":
                    rain = True
                if p == 'snow':
                    snow = True

            self.display.clear_disp()

            displayMatrix = 0
            if rain:
                self.display.set_raw64(ICONS['rain'], displayMatrix)
                displayMatrix += 1
            if snow:
                if displayMatrix == 1:
                    self,display,set_raw64(ICONS['+'], displayMatrix)
                    displayMatrix += 1
                self.display.set_raw64(ICONS['snow'], displayMatrix)
                displayMatrix += 1

            if displayMatrix == 0:
                self.display.displayText("None")
                delayPeriod = 20
            else:
                delayPeriod = 3

            for delay in range(delayPeriod*10):
                if state.interruptAction:
                    break
                time.sleep(0.1)
            if state.interruptAction:
                break

            # If there was no precipitation there is no need to show more data so continue outer loop
            if displayMatrix == 0:
                continue

            precipProbText = str(round(float(precipProb))) + "%"
            self.display.clear_disp()
            self.display.displayText(precipProbText)

            for delay in range(delayPeriod*10):
                if state.interruptAction:
                    break
                time.sleep(0.1)
            if state.interruptAction:
                break

            precipText = str(round(float(precip))) + "€"
            self.display.clear_disp()
            self.display.displayText(precipText)

            for delay in range(delayPeriod*10):
                if state.interruptAction:
                    break
                time.sleep(0.1)
            if state.interruptAction:
                break

            time.sleep(1)

