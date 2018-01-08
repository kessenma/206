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
facebook_access_token = 'EAACEdEose0cBAGZCMBHIQVS2595lZAZBtXXzuHPk5Tv38Rjx2SC6bCG54m41xSRLvs0vgmjOSRhNNtobhgHBtO90t7WUK7uZCCP7lkEYkqM9i9gFgjIFxLZBw4iIQsPM7zx1d0lyrknnCuc6sUI9NtJTLAZBbBbHAI0ZALDWKrl96WeZAjfz54BmGjPbBs9z5883BlckIb7JGZAHVo6H7Gy1R'
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
    unique_identifier = {"access_token": facebook_access_token, "limit": None, 'fields': "id, status_type, message, created_time"}
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

# Plot data for Facebook
facebook_info = [plotly.graph_objs.Bar(x=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
y = [len(sun), len(mon), len(tue), len(wed), len(thu), len(fri), len(sat)])]


layout = plotly.graph_objs.Layout(barmode='group', xaxis=dict(title='Day of Week', titlefont=dict(family='Arial, sans-serif',
size=18, color='lightgrey'), exponentformat='e', showexponent='All'), yaxis=dict(title='Temperature (F)',
titlefont=dict(family='Arial, sans-serif', size=18, color='lightgrey'), exponentformat='e', showexponent='All'))

fig = plotly.graph_objs.Figure(data=data, layout=layout)
plotly.plotly.iplot(fig, filename = 'Weekly Weather Data')

# data = plotly.Data([facebook_info])
plotly.plotly.iplot(facebook_info, filename = 'Total # of Facebook Posts by Day')


















