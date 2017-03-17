"""

	Lambda function to be run on AWS Lambda serverless compute platform; called by the AWS API gateway on the register endpoint.


	Note boto provides an interface to directly write the text string to an S3 object; may be worth a look...


	Robert Curran 16/3/17
	robert@robertcurran.co.uk 

"""

import boto3
import random



"""
	lambda_handler

	Called by the AWS lambda service to compleate the registration process

"""
def lambda_handler(event, context):
	
	s3 = boto3.resource('s3')
	
	bucket = s3.Bucket('arroneventditribution')

	jsonContent = generateJSON()

	createNewFile("/tmp/taekwondo.txt", jsonContent)

	# Generate the new file name
	newFileName = getFileName()
	
	# Upload the new file to S3
	bucket.upload_file('/tmp/taekwondo.txt', newFileName)


	hello_key = bucket.get_key(newFileName)
	hello_key.set_canned_acl('public-read')


	# Return a https link to the new file for use in the polling
	# Interestingly there is not a param avlible for the buclet URI...
	return newFileName


"""
	createNewFile

	Creates the new JSON file for uplaoding to S3

"""
def createNewFile(file, contents):

	file = open(file,"w") 
	
	file.write(contents)
	
	file.close() 




def generateJSON():

	jsonContent = """
	{
	'pollDelay' : 60
	}

	"""
	return jsonContent


def getFileName():

	# Get a new psudo random ID
	UserID = random.randrange(0, 99999999999999999999)
	# There are a whole number of issues in the above stattment. I'm Ignoring them.
	
	# Return the new (hopefuly) unique file name
	return 'user-' + str(UserID)