from forecastiopy import *

fio = ForecastIO.ForecastIO('80702cc5f70100072a7aa990299bd2b5', 40.7128, -74.0060)
current = FIOCurrently.FIOCurrently(fio)
print() 'temperature:', current.temperature