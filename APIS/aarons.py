import calendar
import json
import plotly
import requests
import sqlite3
from datetime import datetime as dt

# Set up weather access token
weather_access_token = '80702cc5f70100072a7aa990299bd2b5'

# Set up the caching pattern start -- the dictionary and the try/except statement.
CACHE_FNAME = "darksky_cache.json"
try:
    cache_file = open(CACHE_FNAME, 'r') # Read file
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents) # Add to dictionary
    cache_file.close() # Close file
except:
    CACHE_DICTION = {}

# Function to get data
def get_weather_data(latitude, longitude):
    base_url = 'https://api.darksky.net/forecast/'
    api_key = '80702cc5f70100072a7aa990299bd2b5'
    latitude = str(latitude)
    longitude = str(longitude)
    full_url = base_url + api_key + '/' + latitude + ',' + longitude

    response = requests.get(full_url)
    data = json.loads(response.text)
    daily = data['daily']['data']
    return daily

# Invocation
# The latitude and longitude currently used is Ann Arbor's
# To display weather from other countries, change the latitude and the longitude
darksky_cache = get_weather_data('42.280841', '-83.738115')
info = []

# Connect database and load data into database
conn = sqlite3.connect('darksky.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Weather')
cur.execute('CREATE TABLE Weather (summary VARCHAR, temperatureHigh NUMBER, temperatureLow NUMBER)')
for weather in darksky_cache:
    tup = (weather["summary"], weather["temperatureHigh"], weather["temperatureLow"])
    info.append(dt.fromtimestamp(weather['time']))
    cur.execute('INSERT OR IGNORE INTO Weather (summary, temperatureHigh, temperatureLow) VALUES (?, ?, ?)', tup)

conn.commit()

# Create plotly graph
# Create an empty dictionary for the days of the week
days_weather = {}
for i in darksky_cache:
    time_stamp = dt.fromtimestamp(i['time'])
    day_of_week = dt.date(time_stamp).weekday()

    if day_of_week == 0:
        days_weather["Monday"] = (i["temperatureHigh"], i["temperatureLow"])
    elif day_of_week == 1:
        days_weather["Tuesday"] = (i["temperatureHigh"], i["temperatureLow"])
    elif day_of_week == 2:
        days_weather["Wednesday"] = (i["temperatureHigh"], i["temperatureLow"])
    elif day_of_week == 3:
        days_weather["Thursday"] = (i["temperatureHigh"], i["temperatureLow"])
    elif day_of_week == 4:
        days_weather["Friday"] = (i["temperatureHigh"], i["temperatureLow"])
    elif day_of_week == 5:
        days_weather["Saturday"] = (i["temperatureHigh"], i["temperatureLow"])
    elif day_of_week == 6 and "Sunday" not in days_weather:
        days_weather["Sunday"] = (i["temperatureHigh"], i["temperatureLow"])

high_temp = []
for day in days_weather.items():
    high_temp.append(day[1][0])

low_temp = []
for day in days_weather.items():
    low_temp.append(day[1][1])

# Plotly API
plotly.tools.set_credentials_file(username = 'alonmelon25', api_key = 'PmSfJAhSMgo0KNMV7mWU')
plotly.tools.set_config_file(world_readable = True)

# Plot data for Darksky
weather_high = plotly.graph_objs.Scatter(x=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
y = high_temp, name = "High Temp")
weather_low = plotly.graph_objs.Scatter(x=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
y = low_temp, name = "Low Temp")

data = [weather_high, weather_low]

# Visualization for a double bar graph
layout = plotly.graph_objs.Layout(barmode='group', xaxis=dict(title='Day of Week', titlefont=dict(family='Arial, sans-serif',
size=18, color='lightgrey'), exponentformat='e', showexponent='All'), yaxis=dict(title='Temperature (F)',
titlefont=dict(family='Arial, sans-serif', size=18, color='lightgrey'), exponentformat='e', showexponent='All'))

fig = plotly.graph_objs.Figure(data=data, layout=layout)
plotly.plotly.iplot(fig, filename = 'Weekly Weather Data')
