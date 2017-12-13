
import urllib.request
import urllib.parse

try:
	url = 'https://api.darksky.net/forecast/80702cc5f70100072a7aa990299bd2b5/42.2808,-83.7430,1990120500?exclude=hourly'
	req = urllib.request.Request(url)
	resp = urllib.request.urlopen(req)
	respData = resp.read()

	saveFile = open('Weatherdata.db','w')
	saveFile.write(str(respData))
	saveFile.close()

except Exception as e:
	print(str(e))

'''
url = 'http://pythonprogramming.net'
values = {'s':'basic',
			'submit':'search'}

data = urllib.parse.urlencode(values)
data = data.encode('utf-8')
req = urllib.request.Request(url,data)
resp = urllib.request.urlopen(req)
respData = resp.read()

print(respData)
'''
#x = urllib.request.urlopen('https://google.com')
#print (x.read())

'''
## 
VIDE0 #1
"Python Web Programming - Urllib Requests"
https://www.youtube.com/watch?v=Su4nRkiW2NQ&t=9s


values = {'q':'python programming tutorials'}

data = urllib.parse.urlencode(values)
url = 'https://www.google.com/search?q='+data
#data = data.encode('utf-8')

req = urllib.request.Requests(url)
resp = urllib.request.urlopen(req)
resp_data = resp.read()

print (resp_data)





api_key = '80702cc5f70100072a7aa990299bd2b5'

response = urllib2.urlopen('https://api.darksky.net/forecast/80702cc5f70100072a7aa990299bd2b5/42.2808,-83.7430,1990120500?exclude=hourly')
html = response.read()

print.url 
'''