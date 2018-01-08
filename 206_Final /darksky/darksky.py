import calendar
import json
import plotly
import requests
import sqlite3
from datetime import datetime as dt

# Set up weather access token
weather_access_token = '80702cc5f70100072a7aa990299bd2b5'
#Don't have to refresh very often/at all. User has 1,000 free calls a day. 

# caching pattern using the same caching pattern as 
# https://github.com/KyleE-School/206/blob/master/SQLite%20/main.py
CACHE_FNAME = "darksky_cache.json"
try:
    cache_file = open(CACHE_FNAME, 'r') # r = read file
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
#This is also how the HTTPS request acts. If I wanted to add parameters I could do so by adding a ,?, with the 
#Parameters I want. I could request only hourly data, preciptation etc. ATM the request is calling for 
#all of the infomration Darksky has and then manipulating it later down in the code. 

    response = requests.get(full_url)
    data = json.loads(response.text)
    daily = data['daily']['data']
    return daily
#    ^^ Here the function is returning the daily temperature. 


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

# https://github.com/KyleE-School/206/blob/master/SQLite%20/main.py
# https://www.python-course.eu/sql_python.php
#https://books.trinket.io/pfe/13-web.html <--- VERY helpful

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
plotly.tools.set_credentials_file(username = 'kessenma', api_key = 'KGuLUQNPjKtvlrjgpmCn')
plotly.tools.set_config_file(world_readable = True)

# Plot data for Darksky
weather_high = plotly.graph_objs.Scatter(x=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
y = high_temp, name = "High Temp")
weather_low = plotly.graph_objs.Scatter(x=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
y = low_temp, name = "Low Temp")

data = [weather_high, weather_low]

# Visualization for a double bar graph
#https://plot.ly/python/

#~~~~~~FORMATTING~~~~~~~~
layout = plotly.graph_objs.Layout(barmode='group', xaxis=dict(title='DAY OF WEEK', titlefont=dict(family='Futura, sans-serif',
size=30, color='lightblue'), exponentformat='e', showexponent='All'), yaxis=dict(title='Temperature (F)',
titlefont=dict(family='Futura, sans-serif', size=18, color='lightblue'), exponentformat='e', showexponent='All'))
#~~~~~~FORMATTING~~~~~~~


fig = plotly.graph_objs.Figure(data=data, layout=layout)
plotly.plotly.plot(fig, filename = 'Weekly Weather Data')