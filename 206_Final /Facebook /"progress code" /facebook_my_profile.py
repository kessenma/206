import os
import json 
import facebook
import FB_info 



FACEBOOK_TEMP_TOKEN = FB_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = faecbook.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
'''
1.) get your access token from FB GRAPH API
2.) type into your terminal: FACEBOOK_ACCESS_TOKEN=<ACCESS TOKEN HERE W NO SPACE OR QUOTATION MARKS>

''' 
##
FACEBOOK_TEMP_TOKEN = 'EAACEdEose0cBAJwkpyq9CSxrRwBBZAEe0PyvD4ysRMXXY1KVm0nEZC2ZABendZByO1LAnO0iXy8bM27A7Ky1mQUfUYTuWZBQVlrsfKjHd1N5QFhhDusmRtUVdsCJlGQscevRggtts2Y9ixkq7lx5KwAoR2KgzwpCdhhJquQ480HZBpim695xYcY4oU2YvtHzZAXLJvH5ZAIP65hnEHvwytIH'

if __name__ == '__main__':
	token = os.environ.get('FACEBOOK_TEMP_TOKEN')

	graph = facebook.GraphAPI(token)
	profile = graph.get_object('me', fields='name, location')

	print(json.dumps(profile, indent=4))