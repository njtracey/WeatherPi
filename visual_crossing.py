######################################################################
#
# Class for abstracting fetching weather data from VisualCrossing
#
# (c) GrumpyFerret - Nigel Tracey
#
######################################################################

import requests
import json
import threading
import visual_crossing_apikey
import time

class WeatherData():
    def __init__(self, temp, feelslike, precip, precipprob, snow, snowdepth, preciptype,
            windspeed, windgust, winddir, cloudcover, uvindex, conditions, icon, description="",
            timestring="", timeepoc=0, sunrise="", sunset="", tempmin=0, tempmax=0, hourly=[]):
        self.timestring = timestring
        self.timeepoc = timeepoc
        self.temp = temp
        self.tempmin = tempmin
        self.tempmax = tempmax
        self.feelslike = feelslike
        self.precip = precip
        self.precipprob = precipprob
        self.snow = snow
        self.snowdepth = snowdepth
        self.preciptype = preciptype
        self.winspeed = windspeed
        self.windgust = windgust
        self.winddir = winddir
        self.cloudcover = cloudcover
        self.uvindex = uvindex
        self.conditions = conditions
        self.description = description
        self.icon = icon
        self.sunrise = sunrise
        self.sunset = sunset
        self.hourly = hourly.copy()

    def __str__(self):
        weatherConditionsString = \
            "Time =      " + str(self.timestring) + "\n" + \
            "Epoc =      " + str(self.timeepoc) + "\n" + \
            "Temp =      " + str(self.temp) + "\n" + \
            "Temp Min =  " + str(self.tempmin) + "\n" + \
            "Temp Max =  " + str(self.tempmax) + "\n" + \
            "Feelslike = " + str(self.feelslike) + "\n" + \
            "Precip =    " + str(self.precip) + "\n" \
            "PrecipProb =" + str(self.precipprob) + "\n" \
            "Snow =      " + str(self.snow) + "\n" \
            "Snow Depth =" + str(self.snowdepth) + "\n" \
            "Precip Type=" + str(self.preciptype) + "\n" \
            "Windspeed = " + str(self.winspeed) + "\n" \
            "Wind Gust = " + str(self.windgust) + "\n" \
            "Wind Dir =  " + str(self.winddir) + "\n" \
            "Cloud Cov = " + str(self.cloudcover) + "\n" \
            "UV Index =  " + str(self.uvindex) + "\n" \
            "Conditions =" + str(self.conditions) + "\n" \
            "Description=" + str(self.description) + "\n" \
            "Icon =      " + str(self.icon) + "\n" \
            "Sun Rise =  " + str(self.sunrise) + "\n" \
            "Sunset =    " + str(self.sunset) + "\n"
        for i, h in enumerate(self.hourly):
            weatherConditionsString = weatherConditionsString + "Hour " + str(i) + ":\n" \
                "  Time =      " + str(h.timestring) + "\n" + \
                "  Epoc =      " + str(h.timeepoc) + "\n" + \
                "  Temp =      " + str(h.temp) + "\n" + \
                "  Feelslike = " + str(h.feelslike) + "\n" + \
                "  Precip =    " + str(h.precip) + "\n" \
                "  PrecipProb =" + str(h.precipprob) + "\n" \
                "  Snow =      " + str(h.snow) + "\n" \
                "  Snow Depth =" + str(h.snowdepth) + "\n" \
                "  Precip Type=" + str(h.preciptype) + "\n" \
                "  Windspeed = " + str(h.winspeed) + "\n" \
                "  Wind Gust = " + str(h.windgust) + "\n" \
                "  Wind Dir =  " + str(h.winddir) + "\n" \
                "  Cloud Cov = " + str(h.cloudcover) + "\n" \
                "  UV Index =  " + str(h.uvindex) + "\n" \
                "  Conditions =" + str(h.conditions) + "\n" \
                "  Icon =      " + str(h.icon) + "\n"
        return weatherConditionsString

    def printTemp(self, hourly=False):
        print(str(self.temp), end="")
        if hourly:
            print(" hourly: ", end="")
            for h in self.hourly:
                print(str(h.temp) + ", ", end="")
        print(".")

class VisualCrossing():
    BASE_URL = "https://weather.visualcrossing.com"
    REQUEST_DETAILS1 = "/VisualCrossingWebServices/rest/services/timeline/"
    REQUEST_DETAILS2 = "/next4days?include=hours%2Ccurrent%2Cdays&key="
    REQUEST_DETAILS3 = "&unitGroup=uk&iconSet=icons2&contentType=json"
    REQUEST_DETAILS4 = "/today?include=current&key="

    def __init__(self, apikey):
        self.apikey = apikey
        self.locationName = None
        self.locationLatLong = None
        self.subLocations = dict()
        self.currentWeatherData = None
        self.dailyWeatherData = []
        self.currentSubWeatherData = dict()
        self.updateFrequency = 300
        self.terminateThread = False
        self.weatherThread = None
        self.weatherMutex = threading.Lock()
        self.weatherDataAccessError = False
        self.weatherDataAvailable = False

    def setLocation(self, name, location):
        self.locationName = name
        self.locationLatLong = location

    def addSublocations(self, name, location):
        self.subLocations[name] = location

    def resetSublocations(self):
        self.subLocations = dict()

    def processWeatherData(self, jsonWeather):
        # Clear the previous cached weather data
        self.dailyWeatherData = []

        # Extract the Current Weather into the cache
        currentWeather = jsonWeather["currentConditions"]
        self.currentWeatherData = WeatherData(
                currentWeather["temp"],
                currentWeather["feelslike"],
                currentWeather["precip"],
                currentWeather["precipprob"],
                currentWeather["snow"],
                currentWeather["snowdepth"],
                currentWeather["preciptype"],
                currentWeather["windspeed"],
                currentWeather["windgust"],
                currentWeather["winddir"],
                currentWeather["cloudcover"],
                currentWeather["uvindex"],
                currentWeather["conditions"],
                currentWeather["icon"],
                sunrise = currentWeather["sunrise"],
                sunset = currentWeather["sunset"],
                timestring = currentWeather["datetime"],
                timeepoc = currentWeather["datetimeEpoch"]
                )

        for day in jsonWeather["days"]:
            hourlyWeatherData = []
            for hour in day["hours"]:
                hourlyWeatherData.append(WeatherData(
                    hour["temp"],
                    hour["feelslike"],
                    hour["precip"],
                    hour["precipprob"],
                    hour["snow"],
                    hour["snowdepth"],
                    hour["preciptype"],
                    hour["windspeed"],
                    hour["windgust"],
                    hour["winddir"],
                    hour["cloudcover"],
                    hour["uvindex"],
                    hour["conditions"],
                    hour["icon"],
                    timestring = hour["datetime"],
                    timeepoc = hour["datetimeEpoch"]
                    ))

            newDailyWeatherData = WeatherData(
                day["temp"],
                day["feelslike"],
                day["precip"],
                day["precipprob"],
                day["snow"],
                day["snowdepth"],
                day["preciptype"],
                day["windspeed"],
                day["windgust"],
                day["winddir"],
                day["cloudcover"],
                day["uvindex"],
                day["conditions"],
                day["icon"],
                description = day["description"],
                sunrise = day["sunrise"],
                sunset = day["sunset"],
                timestring = day["datetime"],
                timeepoc = day["datetimeEpoch"],
                tempmin = day["tempmin"],
                tempmax = day["tempmax"],
                hourly = hourlyWeatherData
                )
            self.dailyWeatherData.append(newDailyWeatherData)

    def processSublocationWeatherData(self, jsonWeather, name):
        # Extract the Current Weather into the cache
        currentWeather = jsonWeather["currentConditions"]
        self.currentSubWeatherData[name] = WeatherData(
                currentWeather["temp"],
                currentWeather["feelslike"],
                currentWeather["precip"],
                currentWeather["precipprob"],
                currentWeather["snow"],
                currentWeather["snowdepth"],
                currentWeather["preciptype"],
                currentWeather["windspeed"],
                currentWeather["windgust"],
                currentWeather["winddir"],
                currentWeather["cloudcover"],
                currentWeather["uvindex"],
                currentWeather["conditions"],
                currentWeather["icon"],
                sunrise = currentWeather["sunrise"],
                sunset = currentWeather["sunset"]
                )

    def getWeatherData(self):
        self.weatherDataAccessError = False

        REQUEST_URL = VisualCrossing.BASE_URL
        REQUEST = VisualCrossing.REQUEST_DETAILS1 + self.locationLatLong + VisualCrossing.REQUEST_DETAILS2 + self.apikey + VisualCrossing.REQUEST_DETAILS3

        try:
            r = requests.get(REQUEST_URL + REQUEST)
        except:
            print("Error   " + REQUEST)
            self.weatherDataAccessError = True
            self.weatherDataAvailable = False
        else:
            try:
                self.processWeatherData(r.json())
            except:
                print("Error processing Weather Data")
                self.weatherDataAccessError = True
                self.weatherDataAvailable = False

        for name, latlong in self.subLocations.items():
            REQUEST = VisualCrossing.REQUEST_DETAILS1 + latlong + VisualCrossing.REQUEST_DETAILS4 + self.apikey + VisualCrossing.REQUEST_DETAILS3
            try:
                r = requests.get(REQUEST_URL + REQUEST)
            except:
                print("Error   " + REQUEST)
                self.weatherDataAccessError = True
                self.weatherDataAvailable = False
            else:
                try:
                    self.processSublocationWeatherData(r.json(), name)
                except:
                    print("Error processing Sublocation Weather Data")
                    self.weatherDataAccessError = True
                    self.weatherDataAvailable = False

        if self.weatherDataAccessError == False:
                self.weatherDataAvailable = True

    def pollForWeather(self):
        pollingPeriod=0

        # Get first instance of weather data now
        self.weatherMutex.acquire()
        self.getWeatherData()
        self.weatherMutex.release()

        while True:
            # Continue to update the weather based on the set update Frequency
            if pollingPeriod == self.updateFrequency:
                pollingPeriod=0
                self.weatherMutex.acquire()
                self.getWeatherData()
                self.weatherMutex.release()
            pollingPeriod+=1
            time.sleep(1)
            if self.terminateThread:
                break

    def stopPollingForWeather(self):
        self.terminateThread=True
        self.weatherThread.join()

    def setPollingPeriod(self,updateFrequency = 300):
        self.updateFrequency = updateFrequency

    def pollForWeatherWithThread(self):
        self.weatherThread = threading.Thread(target=self.pollForWeather, args=(), daemon=True)
        self.weatherThread.start()

# Set-up and test framework for the VisualCrossing API Class
if __name__ == "__main__":
    myvisualcrossing = VisualCrossing(visual_crossing_apikey.myVisualCrossingAPIKey)
    myvisualcrossing.setLocation("Liverpool", "53.39079,-2.9055259")
    myvisualcrossing.addSublocations("York", "53.9270239,-1.0741348")
    myvisualcrossing.addSublocations("London", "51.4892971,-0.1132849")
    myvisualcrossing.setPollingPeriod(20)
    myvisualcrossing.pollForWeatherWithThread()
    time.sleep(5)

    while True:
        # Print Stuff Out to Validate
        print("The Extracted Current Weather is: ", end="")
        myvisualcrossing.weatherMutex.acquire()
        myvisualcrossing.currentWeatherData.printTemp()
        myvisualcrossing.weatherMutex.release()
        time.sleep(10)
