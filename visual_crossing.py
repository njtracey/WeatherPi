######################################################################
#
# Class for abstracting fetching weather data from VisualCrossing
#
# (c) GrumpyFerret - Nigel Tracey
#
######################################################################

import requests
import json
import visual_crossing_apikey

class WeatherData():
    def __init__(self, temp, feelslike, precip, precipprob, snow, snowdepth, preciptype,
            windspeed, windgust, winddir, cloudcover, uvindex, conditions, icon,
            sunrise=None, sunset=None, hourly=[]):
        self.temp = temp
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
        self.icon = icon
        self.sunrise = sunrise
        self.sunset = sunset
        self.hourly = hourly.copy()

    def __str__(self):
        weatherConditionsString = \
            "Temp =      " + str(self.temp) + "\n" + \
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
            "Icon =      " + str(self.icon) + "\n" \
            "Sun Rise =  " + str(self.sunrise) + "\n" \
            "Sunset =    " + str(self.sunset) + "\n"
        for i, h in enumerate(self.hourly):
            weatherConditionsString = weatherConditionsString + "Hour " + str(i) + ":\n" \
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
    REQUEST_DETAILS3 = "&unitGroup=uk&contentType=json"
    REQUEST_DETAILS4 = "/today?include=current&key="

    def __init__(self, apikey):
        self.apikey = apikey
        self.locationName = None
        self.locationLatLong = None
        self.subLocations = dict()
        self.currentWeatherData = None
        self.dailyWeatherData = []
        self.currentSubWeatherData = dict()

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
                currentWeather["sunrise"],
                currentWeather["sunset"]
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
                sunrise = day["sunrise"],
                sunset = day["sunset"],
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
                currentWeather["sunrise"],
                currentWeather["sunset"]
                )

    def getWeatherData(self):
        REQUEST_URL = VisualCrossing.BASE_URL

        REQUEST = VisualCrossing.REQUEST_DETAILS1 + self.locationLatLong + VisualCrossing.REQUEST_DETAILS2 + self.apikey + VisualCrossing.REQUEST_DETAILS3
        print("Getting Weather for " + self.locationName + ": ")
        try:
            print("   " + REQUEST)
            r = requests.get(REQUEST_URL + REQUEST)
        except:
            print("Error")
        else:
            self.processWeatherData(r.json())

        for name, latlong in self.subLocations.items():
            REQUEST = VisualCrossing.REQUEST_DETAILS1 + latlong + VisualCrossing.REQUEST_DETAILS4 + self.apikey + VisualCrossing.REQUEST_DETAILS3
            print("Getting Current Weather Conditions for " + name + ": ")
            try:
                print("   " + REQUEST)
                r = requests.get(REQUEST_URL + REQUEST)
            except:
                print("Error")
            else:
                self.processSublocationWeatherData(r.json(), name)

# Set-up and test framework for the VisualCrossing API Class
myvisualcrossing = VisualCrossing(visual_crossing_apikey.myVisualCrossingAPIKey)
myvisualcrossing.setLocation("Liverpool", "53.39079%2C-2.9055259")
myvisualcrossing.addSublocations("York", "53.9270239,-1.0741348")
myvisualcrossing.addSublocations("London", "51.4892971,-0.1132849")
myvisualcrossing.getWeatherData()

# Print Stuff Out to Validate
print("The Extracted Current Weather is: ", end="")
myvisualcrossing.currentWeatherData.printTemp()
print("The Extracted Daily Weather is: ")
for d in myvisualcrossing.dailyWeatherData:
    d.printTemp(hourly=True)
print("The Sublocation Weather is: ")
for name, weather in myvisualcrossing.currentSubWeatherData.items():
    print("The sublocation weather for " + name + ": ", end="")
    weather.printTemp()
