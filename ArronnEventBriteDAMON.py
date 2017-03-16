import webbrowser
import requests
import time


# Set a display time limit of 3 days
DisplayTimeLimit  = 172800




"""
	Polls the server

	Gets the latest JSON data from the server; returns a dict with the Address and Issued date in unix form
	example:
	{'address': "https://www.google.com", 'issued': 1369550494}
"""
def pollServer():

	# Get the latest JSON from S3:
	r = requests.get('https://s3-eu-west-1.amazonaws.com/arroneventditribution/s3test')

	# Extract the JSON
	latestJSON = r.json()

	addressToOpen = latestJSON["address"] 
	issuedAt = latestJSON["issued"] 

	# Return the aquired data
	return {'address': addressToOpen, 'issued': issuedAt}




"""
	Display

	Displays the passed webaddress on the client device
"""
def display(webAddress):
	# Open the link in the default web browser for this platform
	webbrowser.open(webAddress)






if __name__ == "__main__":

	pollData = pollServer()

	print "Attempting to open: " , pollData["address"]

	# Time differnce between now and issue point
	UnixDiff = (time.time() - pollData["issued"])

	print "The unix diff is: %d "  % UnixDiff

	# Only continue if the message is less than two days old
	if(UnixDiff > 172800):
		
		display(pollData["address"])

	