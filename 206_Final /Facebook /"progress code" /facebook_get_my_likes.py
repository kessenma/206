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
facebook_access_token = 'EAACEdEose0cBADoP9i2Rel84QEYZAq5WrZA7sKhggxykSIfrHqvMNfBNFsRdL9Milv7SYHNnBFC9Rf0wjzuF21c8JKqFFMT2imUBDhVFEGKbbRcHQHmZA5BSRWLQiLtWjGHfuUPrnpdzRFUIkV0ZAcJJKZBezq9ybGoZCfvciOoeenTNhX4FnMgNCeJZA1HEFwZAaN898r1RaudAyJlmJ23m'
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
    unique_identifier = {"access_token": facebook_access_token, "limit": None, 'fields': "id, name, created_time"}
    url = "https://graph.facebook.com/v2.5/me/feed"
# Had to tinker around with the Access token + the limits to get thie one to work, but the documentation for the graph api on FB is helpful


# if the user has a cache file on hand loop through the cached file instead of going online  
    if user in CACHE_DICTION:
        print('Using cached data...')
        facebook_results = CACHE_DICTION[user]
# if the user does not have a cached file retrieve data from the key provided and create a cache file. 
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
# Similaro to projerct three again.  
conn = sqlite3.connect('facebook_likes.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (user_id TEXT, status_type TEXT, name VARCHAR, time_posted DATETIME)')
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
    cur.execute('INSERT OR IGNORE INTO Facebook (user_id, status_type, message, time_posted) VALUES (?, ?, ?, ?)', tup)

conn.commit()


# Create plotly graph
# Creates lists for the days of the week for the proogram to fill in with either cached data or with data aquired from the API. 
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

# Plot data for Facebook
facebook_info = [plotly.graph_objs.Bar(x=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
y = [len(sun), len(mon), len(tue), len(wed), len(thu), len(fri), len(sat)])]


# data = plotly.Data([facebook_info])
plotly.plotly.iplot(facebook_info, filename = 'Total # of Facebook Likes by Day')

#didn't have time to edit this to the extent that I would have liked. I was getting weird diction errors 
#while editing around so I decided to stop. 

















