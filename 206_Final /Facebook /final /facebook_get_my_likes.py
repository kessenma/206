import os
import json 
import facebook 
import requests
import plotly
import sqlite3
import datetime
from datetime import datetime as dt
import plotly.graph_objs as go
import plotly.plotly as py

'''
1.) get your access token from FB GRAPH API @---> https://developers.facebook.com/tools/explorer/
''' 

# Set up Facebook access token
# Facebook access token expires after a certain period of time. As a general rule of thumb I just grab a new one every time I tinker. 
facebook_access_token = 'EAACEdEose0cBANVy2An5anI6Do3AZAnRaRFuMI3mM5RrZC8kVDDiCxVyZCjqBU5JeYZBX73odmJuOTF5x9ZB3UuDWIkSjWD2Wl1YnRIVROqgC4SYP8io4m8jCa01phETgfeqsYsn4i3us7j1LXy0gY17kuQXEro99oVZCYhXlBjmR4iG9EEVPT7ZB92fVVJquDXErSZCbVHoH3CVyW3yu5qb'
facebook_graph = facebook.GraphAPI(facebook_access_token)
facebook_profile = facebook_graph.get_object("me", fields = 'name, location')

# Set up the caching pattern start -- the dictionary and the try/except statement.
CACHE_FNAME = "facebook_cache.json"
try:
    cache_file = open(CACHE_FNAME, 'r') # Read file
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents) # Add to dictionary
    cache_file.close() # Close file
except:
    CACHE_DICTION = {}

# This function is very similar to the ones from project three. 
# Function to get data
def get_facebook_data(user):
    unique_identifier = {"access_token": facebook_access_token, "limit": 100, "data": "user_likes, name, id, created_time"}
    url = "https://graph.facebook.com/v2.5/me/feed"
# Had to tinker around with the Access token + the limits to get thie one to work, but the documentation for the graph api on FB is helpful


# if user has a cache file in the project file--> loop through the cached file instead of fetching data. 
    if user in CACHE_DICTION:
        print('Using cached data...')
        facebook_results = CACHE_DICTION[user]
# if the user does not have a cached file retrieve data from the authorization key provided and create a 
# cache file + save it with this file.
# if the ket is not updat
    else:
        print("Fetching data...")
        results = requests.get(url, params = unique_identifier) #params = parameter
        CACHE_DICTION[user] = json.loads(results.text)
        facebook_results = CACHE_DICTION[user]
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME, 'w') # W = write. the program is going to write the data it collects from your profile and write it. 
        f.write(dumped_json_cache)
        f.close() #Close the open file
    return facebook_results 


facebook_json = get_facebook_data("Kyle Essenmacher") 

info = []
data = facebook_json['data']

# Connect database and load data into database.
# This is relativley the same as dark sky just with a littl bit more technicality.
# Similar to to project three again.  
conn = sqlite3.connect('facebook_likes.sqlite')
cur = conn.cursor()


# This part of the program is creating a SQl database using the same 
# "fields" given above-- Status_type, name, & time_posted 
cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (user_id TEXT, status_type TEXT, name VARCHAR, time_liked DATETIME)')
for i in data:
    if "name" in i:
        tup_message = i["name"]
    else:
        tup_message = None

    if "status_type" in i:
        tup_status = i["status_type"]
    else:
        tup_status = None
    tup = (i['id'], tup_status, tup_message, str(dt.strptime(i['created_time'][:-5], '%Y-%m-%dT%H:%M:%S')))
    info.append(dt.strptime(i['created_time'][:-5], '%Y-%m-%dT%H:%M:%S'))
    cur.execute('INSERT OR IGNORE INTO Facebook (user_id, status_type, name, time_liked) VALUES (?, ?, ?, ?)', tup)

conn.commit()


# Create plotly graph
# Creates lists for the days of the week for the proogram to fill in with either cached data or with data aquired from FB Graph. 
sun = []
mon = []
tue = []
wed = []
thu = []
fri = []
sat = []

for i in info:
    day_of_week = dt.date(i).weekday()

# Separating days of week
# https://en.wikipedia.org/wiki/SQL
# https://books.trinket.io/pfe/15-database.html
    if day_of_week == 0:
        sun.append(day_of_week)
    elif day_of_week == 1:
        mon.append(day_of_week)
    elif day_of_week == 2:
        tue.append(day_of_week)
    elif day_of_week == 3:
        wed.append(day_of_week)
    elif day_of_week == 4:
        thu.append(day_of_week)
    elif day_of_week == 5:
        fri.append(day_of_week)
    else:
        sat.append(day_of_week)

# Plotly API
# Can get an API Key from https://plot.ly/settings/api Free service and is relativley easy to set up. 
plotly.tools.set_credentials_file(username = 'kessenma', api_key = 'KGuLUQNPjKtvlrjgpmCn')
plotly.tools.set_config_file(world_readable = True)

# Plot data for Facebook
facebook_info = [plotly.graph_objs.Bar(x=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
y = [len(sun), len(mon), len(tue), len(wed), len(thu), len(fri), len(sat)])]


# data = plotly.Data([facebook_info])
plotly.plotly.plot(facebook_info, filename = '#3 Last 100 FB LIKES by Day')

#didn't have time to edit this to the extent that I would have liked. I was getting weird diction errors 
#while editing around so I decided to stop. 

















