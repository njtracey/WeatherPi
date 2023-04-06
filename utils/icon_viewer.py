from rpi_weather_hw import RpiWeatherHW

def displayIcon(value):
    print("BITMAP = [")
    for y in range(8):
        row_byte = value>>(8*y)
        print("   [", end="")
        for x in range(8):
            pixel_bit = row_byte>>x&1 
            print(pixel_bit, end=", ")
        print("],")

    print("]")

iconValue = 0x3c4299858599423c

displayIcon(iconValue)

display = RpiWeatherHW()

display.set_raw64(iconValue, 0)

