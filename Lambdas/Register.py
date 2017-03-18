"""

	Lambda function to be run on AWS Lambda serverless compute platform; called by the AWS API gateway on the register endpoint.
	The lambda will require access to the relevent S3 bucket, a sample policy for this is included bellow:

	{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
            	"s3:ListBucket",
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::arroneventditribution/*"
            ]
        }
    ]
	}

	The service will also require the 'AWSLambdaBasicExecutionRole' canned policy for access to the logging stream.

	Note boto provides an interface to directly write the text string to an S3 object; may be worth a look...


	Robert Curran 16/3/17
	robert@robertcurran.co.uk 

"""

import boto3
import random
import time
import json

# Put the bucket to be used here
bucketName = 'arroneventditribution'
# Poll Delay in seconds
pollDelay = 60


"""
	lambda_handler

	Called by the AWS lambda service to compleate the registration process

"""
def lambda_handler(event, context):
	
	s3 = boto3.resource('s3')
	
	bucket = s3.Bucket(bucketName)

	jsonContent = generateJSON()

	createNewFile("/tmp/taekwondo.txt", jsonContent)

	# Generate the new file name
	newFileName = getFileName()
	
	# Upload the new file to S3
	bucket.upload_file('/tmp/taekwondo.txt', newFileName)

	# Get the S3 Client, used to add ACL to bucket objects
	client = boto3.client('s3')

	# Make the new object public read
	response = client.put_object_acl(
    	ACL='public-read',
    	Bucket=bucketName,
    	Key=newFileName,
	)

	# Return a https link to the new file for use in the polling
	# Interestingly there is not a param avlible for the buclet URI...
	accessURL = 'https://s3-eu-west-1.amazonaws.com/' + bucketName + '/' + newFileName

	return json.dumps({"accessURL" : accessURL , "iD" : newFileName}, sort_keys=True)


"""
	createNewFile

	Creates the new JSON file for uplaoding to S3

"""
def createNewFile(file, contents):

	file = open(file,"w") 
	
	file.write(contents)
	
	file.close() 




def generateJSON():
	
	# This will likley be refactored out at this point soon...

	return json.dumps({"pollDelay": pollDelay, "registerdAt" : time.time()}, sort_keys=True)


"""
	getFileName

	Generates the name for the file/key
"""
def getFileName():

	# Get a new psudo random ID
	UserID = random.randrange(0, 99999999999999999999)
	# There are a whole number of issues in the above stattment. I'm Ignoring them.
	
	# Return the new (hopefuly) unique file name
	return 'user-' + str(UserID)