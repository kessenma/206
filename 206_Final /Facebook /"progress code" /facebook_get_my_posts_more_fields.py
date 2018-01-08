import os
import json 
import facebook 
import requests

'''
1.) get your access token from FB GRAPH API
2.) type into your terminal: FACEBOOK_ACCESS_TOKEN=<ACCESS TOKEN> <--- WITH NO SPACE OR QUOTATION MARKS!! literally just the token
        ^^before you run this program.              ^^^this access token and the one below it are the same!!

''' 
#gotta replace this token often
FACEBOOK_TEMP_TOKEN = 'EAACEdEose0cBAMT0LAYWOBZBgnCoYPlWPhCbzaGxRjdc55wzGnZAyn7oLxvkNv5ExBxYzKKmEq1gE1wtwO4YtBK0mih0MkaWDigxIPEZBvqc9Pu61ZCeIKd05ueuNThjgbhunjaykOMmaJ3tALxLZCwhtXBjZAqVLPnKZBueBJkUoQx7YuJY1I4qzND3r2nLQiuleh0BwoMwDzZAyISAaih6X6sOFWaah3CcDhVa0OBzZBYcLxkcuIoUc'
#gotta replace this token often

if __name__ == '__main__':
	token = os.environ.get('FACEBOOK_TEMP_TOKEN')

	graph = facebook.GraphAPI(token)
	all_fields = [
	'message',
	'created_time',
	'description',
	'caption',
	'link',
	'place',
	'status_type',
	]
	all_fields = ','.join(all_fields)
	posts = graph.get_connections('me', 'posts', fields=all_fields)

	while True: # keep paginating
		try:
			with open('my_posts2.jsonl','a') as f:
				for post in posts['data']:
					f.write(json.dumps(post)+"\n")
				#get next page 
				posts = requests.get(posts['paging']['next']).json()
		except KeyError:
				#no more pages, breaks the loop
			break 
















