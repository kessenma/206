import datetime
import dateutil.parser
import facebook
import json
import plotly
import random
import requests
import urllib
import sqlite3
import webbrowser

from datetime import datetime as dt

#Set up access token 
Access_token= 'EAACEdEose0cBAMZCLY3tVwgIweiiuu6IoWVZCzAlqBxRiO919T8bhOrzC5e8RByQPJse140ZCIcbcZBHkBAlUhdGbntZA5kMLzq0bW6JXfL15DZAaOZBqdi0FkvZBgTP7e2mSIrHd3ZAZBBM0zZCd0kRNKPXktXdXoddEeyptZA1EZBZBf4C7aSo5qpbS3wGPMiZBhdolkZD'
Facebook_graph = Facebook.GraphAPI(Access_token)
Facebook_profile= Facebook_graph.get_object("me", fields = 'name, location')

# Set up caching using try/exempt statements 
CACHE_FNAME = "facebook)_cache.json"
try: 
	cache_file = open(CACHE_FNAME, 'r') #Read File 
	cace_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents) #Add to dictionary 
except:
	CACHE_DICTION = {}

#Function to get data 
def get_facebook_data(user):
	unique_identifier = {"Access_token" : Access_token, "limit":100, 'fields': "id, status_type, likes, created_time"}
	url = "https://graph.facebook.com/v2.3/me/feed"

	if user in CACHE_DICTION: 
		print('Using Cached data')
		facebook_results = CACHE_DICTION[user]
	else 
		print("fetching data...")
		results = requests.get(url, params = unique_identifier)
		CACHE_DICTION[user] = json.loads(results.text)
		facebook_results =CACHE_DICTION[user]
		dumped_json_cache = json.dumps(CACHE_DICTION)
		f = open(CACHE_FNAME, 'w') #writes the file 
		f.write(dumped_json_cache)
		f.close() #closes the opened file
	return facebook results


#Invocation 
facebook_json = get_facebook_data("Kyle Essenmacher")

info = []
data = facebook_json['data']

#Connect database and local data into database 
conn = sqlite3.connect('facebook.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE FACEBOOK (user_id TEXT, status_type LIKE, message VARCHAR, time_posted DATETIME')
for i in data: 
	if 






## Connect database and load data into database










