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

BITMAP = [
   [0, 1, 1, 0, 0, 1, 1, 0, ],
   [0, 1, 1, 0, 0, 1, 1, 0, ],
   [0, 0, 0, 0, 0, 0, 0, 0, ],
   [0, 0, 0, 0, 0, 0, 0, 0, ],
   [0, 0, 0, 1, 1, 0, 0, 0, ],
   [0, 1, 1, 0, 0, 1, 1, 0, ],
   [0, 1, 0, 0, 0, 0, 1, 0, ],
   [0, 0, 0, 0, 0, 0, 0, 0, ],
]

value = 0
for y,row in enumerate(BITMAP):
    row_byte = 0
    for x,bit in enumerate(row):
        row_byte += bit<<x
    value += row_byte<<(8*y)
print("0x"+format(value,'02x'))

iconValue = value
displayIcon(iconValue)

display = RpiWeatherHW()
display.set_raw64(iconValue, 0)

