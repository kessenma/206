import json
time = 631170000
for i in range(100):
	response = <your api call + time>
	json_data = json.loads(response.text)
	<store this json object somewhere - either a list to be written to a csv or as an insert statement to a table>
	# WARNING - you may have to scrub single or double quotes from json_data before inserting into a table
	# json_string_dirty = str(json_data)
	# json_string = json_string_dirty.replace("'","`")
        conn.execute("INSERT INTO dark_sky_data (date,json_data) VALUES ('"+ time +"', '"+ json_data+"');")
#     conn.commit()
	# increment you TIME variable by one day (86400 seconds)
	TIME += 86400