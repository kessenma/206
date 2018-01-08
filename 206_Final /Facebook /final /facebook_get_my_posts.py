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
# Facebook access token expires after a certain period of time, need to renew often
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


# Function to get data
def get_facebook_data(user):
    unique_identifier = {"access_token": facebook_access_token, "limit": 1000, 'fields': "id, status_type, message, created_time"}
    url = "https://graph.facebook.com/v2.3/me/feed"

    if user in CACHE_DICTION:
        print('Using cached data...')
        facebook_results = CACHE_DICTION[user]
    else:
        print("Fetching data...")
        results = requests.get(url, params = unique_identifier)
        CACHE_DICTION[user] = json.loads(results.text)
        facebook_results = CACHE_DICTION[user]
        dumped_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME, 'w')
        f.write(dumped_json_cache)
        f.close() #Close the open file
    return facebook_results


# Invocation
facebook_json = get_facebook_data("Kyle Essenmacher")

info = []
data = facebook_json['data']

# Connect database and load data into database
conn = sqlite3.connect('facebook.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (user_id TEXT, status_type TEXT, message VARCHAR, time_posted DATETIME)')
for i in data:
    if "message" in i:
        tup_message = i["message"]
    else:
        tup_message = None

    if "status_type" in i:
        tup_status = i["status_type"]
    else:
        tup_status = None
    tup = (i['id'], tup_status, tup_message, str(dt.strptime(i['created_time'][:-5], '%Y-%m-%dT%H:%M:%S')))
    info.append(dt.strptime(i['created_time'][:-5], '%Y-%m-%dT%H:%M:%S'))
    cur.execute('INSERT OR IGNORE INTO Facebook (user_id, status_type, message, time_posted) VALUES (?, ?, ?, ?)', tup)

conn.commit()

# Create plotly graph
# Create empty lists for the days of the week
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
plotly.tools.set_credentials_file(username = 'kessenma', api_key = 'KGuLUQNPjKtvlrjgpmCn')
plotly.tools.set_config_file(world_readable = True)


facebook_info = [plotly.graph_objs.Bar(x=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
y = [len(sun), len(mon), len(tue), len(wed), len(thu), len(fri), len(sat)])]
# data = plotly.Data([facebook_info])
plotly.plotly.plot(facebook_info, filename = '#2 ALL of My FB POSTS by Day')


















