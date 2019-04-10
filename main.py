# ########################################################################################
# Khuram Chughtai
# Impulse Intelligence
# Web Minning Operations

# The Following are Library expected to exist with standard python install
import os					# Used for OS related Functions generic across all Platforms
import re					# Regex Library used to help parse out words
import json					# Used to Transform data in JSON Format as expected
import sys					# Used to Call System Functions and Import Classes Correctly
import logging 				# Used to Create File Logging Structure that will Help with Debugging
import requests             # Used to Download Web data and handle headers and act like a browser
import json					# Tools to Handle the output and input to JSON based data
from random import randint	# Used to Randomly generate the time to wait between the requests
from time import sleep		# Function used to pause the program to allow for some wait time between requests
import datetime				# Module Used for Date related functions 

class Nsgclass:
	"""
	Class Created that reads in a given textfile and processes the sentiment analysis on that returning a dict object
	"""
	def __init__(self, name, **kwargs): 
		self.name = name
		self.base =  str(os.path.dirname(os.path.abspath( __file__ )))
		# Reading in Class Arguments
		for key in kwargs:
			# This will look at different Given Arguments Passed by a Class and process them accordingly
			if str(key).lower() == 'given_argument':
				pass
			# This is to initiate the logging Instance for this class to keep a good log 
			elif str(key).lower() == 'logging':
				# The following says an argument was given where the user asked for Logging to be True
				# The following action is depricated to allow for the logging that Teradata Module Does.
				if kwargs[key] == True:
					try:  # Catch Block to create a self logging instance as this is extremely Important to Submit Success or Failure
						if not os.path.exists( self.base + "/logs"):
							os.makedirs(self.base + "/logs")
						self.log = self.createLog(	application=str(self.name),
													applicationpath=str( 'logs/{}.log'.format(self.name)))
						self.log.info("Log Initalized, Class Initalized")
					except Exception as error:
						# The following will Raise a better error that lets us unstand it was caused by Logging Module
						raise ValueError("Not Able to Initiate Log File: {}".format(error))
		
	def createLog(self, application, applicationpath):
		"""
		Base Logging Function created to write output from various functions for better error checking\
		this function is for class use only and not meant to be used by outside user.\n

		@param	application	(str)	Name of the Logging Instance that is to be created
		@param	applicationpath	(str)	Path of the Logging file to which this information will be appended

		@return	mylog	(loggingClass)	Logging Class instance used to write to the log file.
		"""
		mylog = logging.getLogger(application)
		fileHandler = logging.FileHandler(applicationpath)
		fileHandler.setFormatter(logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s'))
		mylog.addHandler(fileHandler)
		mylog.setLevel(logging.DEBUG)
		return mylog

	def replaceBlankSpace(self, myString):
		"""
		Simple Utility function that replaces the blank space in a string with %20

		@param	myString	(str)	String that should have blank spaces reformatted
		"""
		return myString.replace(" ", "%20")

	def downloadURLData(self, urlToSubmit, **kwargs):
		"""
		Download Function for a given URL that runs through twice and logs the results from the request header or raise\
		for the given error that exists causing the URL not to be downloaded.  Allow control over minor changes to allow\
		user to work with the request more efficiently

		@param	urlToSubmit	(str)	This will be the URL that we are submitting our request to for downloads	
		@param	timeout	(int)	This will be in seconds how long we should wait for a timeout Ex: 10 or 20 seconds 
		@param	redirects (bool)	This is for the requests to allow redirects from the URL or not, certain websites redirect url requests
		@param	headers	(dict)	This needs to be a dict that allow the user to modify headers for the request or default headers will be used
		@param	sslVerify	(bool)	This is to check for SSL Certificate verification, might not work for all hosts and networks 
		@param	expectedDataLength	(int)	This is the expected Data Length that the program expects to receieve otherwise it shows data\
			not downloaded as expected
		@returns (str)	URL text that gets returned from a successful request
		"""
		# Default Variables Local to the Function Only
		reqTimeout = 120
		reqRedirects = True
		expectedDataLength = 0
		enoughDataDownloaded = True
		# Trying the Actual Error and will return error caused or raised by the request
		myHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
		reqSSLVerify = False
		for key in kwargs:
			# This will look at different Given Arguments Passed by a Class and process them accordingly
			if str(key).lower() == 'given_argument':
				pass
			elif str(key).lower() == 'timeout':
				reqTimeout = kwargs[key]
			elif str(key).lower() == 'redirects':
				reqRedirects = kwargs[key]
			elif str(key).lower() == 'headers':
				myHeaders = kwargs[key]
			elif str(key).lower() == 'sslverify':
				reqSSLVerify = kwargs[key]
		self.log.info("Values set for URL Request: Timeout {}, Redirects: {}, headers: {}, sslVerification: {}".format( reqTimeout,
																														reqRedirects,
																														myHeaders,
																														reqSSLVerify))
		self.log.info ("Created Following Request URL To Query : {}".format(urlToSubmit))
		try:
			# Establishing URL timeout to 2 Minutes Exactly before we wait any where from 20 to 25 second to send a new request
			response = requests.get(urlToSubmit, 
									allow_redirects=reqRedirects, 	# URL Redirection Accepted or not
									headers=myHeaders, 				# Header Option for URL
									timeout=reqTimeout, 			# Timeout Request for URL
									verify=reqSSLVerify)			# SSL Verification Option
			responseLog = 'Downloaded For {}, At Date {}, Received {} HTML Code, Content Type: {}, Content Length: {}'.format(
										str(urlToSubmit), 					        # This is the Rating Type we are trying to download Data For
										response.headers['Date'],			        # DateTime Format of the Date we are getting Data For
										response.status_code,				        # This is the HTTP Status Code we receive back letting us know it is sucessful
										response.headers['Content-Type'],	        # Letting me know an HTML Webpage was downloaded as I expected
										len(str(response.text))         	        # Letting me know enough data was downloaded as I expected 
										)
			self.log.info(responseLog)
			# Custom Check that looks to see if enough data was returned or if it was a data timeout message
			if (expectedDataLength != 0) and ( len(str(response.text)) < expectedDataLength):
				enoughDataDownloaded = False
				self.log.error("Expected to Receive Minimum of {} Bytes of Data and Received {} Bytes of Data".format(	expectedDataLength, 
																														len(str(response.text))))
			# If it receives a status code of any thing other than a 200 it will submit a request for a second time to see if it get a different response before rasing error
			# Also checking to see if enough Data was returned as was expected before rasising an error as well.
			if (response.status_code != 200  or enoughDataDownloaded == False):
				self.log.error("Due to Failure Retrying to Submit to URL: {}".format(urlTOSubmit))
				# Telling Script to sleep for 20 to 25 second based off the failure of last request
				sleep(randint(20,25))
				# Establishing URL timeout to 2 Minutes Exactly before we wait any where from 20 to 25 second to send a new request
				response = requests.get(urlToSubmit, 
										allow_redirects=reqRedirects, 	# URL Redirection Accepted or not
										headers=myHeaders, 				# Header Option for URL
										timeout=reqTimeout, 			# Timeout Request for URL
										verify=reqSSLVerify)			# SSL Verification Option
				responseLog = 'Downloaded For {}, At Date {}, Received {} HTML Code, Content Type: {}, Content Length: {}'.format(
											str(urlToSubmit), 					        # This is the Rating Type we are trying to download Data For
											response.headers['Date'],			        # DateTime Format of the Date we are getting Data For
											response.status_code,				        # This is the HTTP Status Code we receive back letting us know it is sucessful
											response.headers['Content-Type'],	        # Letting me know an HTML Webpage was downloaded as I expected
											len(str(response.text))         	        # Letting me know enough data was downloaded as I expected 
											)
				self.log.info(responseLog)
				if response.status_code == 200:
					return response.text
				else:
					# This is incase of a Failure it will raise an error for failure
					if (expectedDataLength != 0) and ( len(str(response.text)) < expectedDataLength):
						self.log.error("Expected to Receive Minimum of {} Bytes of Data and Received {} Bytes of Data".format(	expectedDataLength, 
																																len(str(response.text))))
					else:
						self.log.error("Received the following error code back from bad request: {}, with {} Bytes of Data Returned".format(response.status_code, 
																																			len(str(response.text))))
					raise ValueError("No data was downloaded from this request: {}".format(e))
			# Will Return Data if Everything was successful. 
			return response.text
		except Exception as error:
			raise ValueError("No data was downloaded from this request: {}".format(error))

	def createCSVFromSearchData(self, titleList, dataArrays, fileName):
		"""
		This take the downloaded and formatted data and create an csv file

		@param	titleList	(list)	List of titles for csv file ex, ["index", "name", "movie"]
		@param	dataArrays	(list)	List of Lists of data that will be added to array\
			EX: [ ["Data 1", "Data 2", "Data3"],  ["Data 1", "Data 2", "Data3"]]
		@param	fileName	(str)	Name of the csv file we will write to
		"""
		# This checks to see the filename has already not be created
		if not os.path.isfile(self.base + "/" + fileName + ".csv"):
			fileToOpen = self.base + "/" + fileName + ".csv"
		# This will execute if filename already exists
		else:
			# I will be adding Timestamp to FileName Provided to allow for Multiple Files to exist
			# And no file to be overwritten
			fileToOpen = (	self.base + "/" + fileName + 
							datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".csv" )
		with open(fileToOpen, 'w') as outputFile:
			# Will Looks to see that the Title Array Matches the Second List of Data Array
			# To make sure we can write the columns as we expect
			if len(titleList) == len(dataArrays[0]):
				# Writes each element of header to be processes using List Comprehension Style
				outputFile.write(','.join('"{}"'.format(csvHeader) for csvHeader in titleList)+ "\n")
				for dataArray in dataArrays:
					outputFile.write(','.join('"{}"'.format(csvData) for csvData in dataArray)+ "\n" )
			else:
				error = "We have a mismatch in Titles and Data Arrays, TitleArray: {}, DataArray:{}".format( len(titleList),
																											 len(dataArrays[0]))
				self.log.error(error)
				raise ValueError(error)
	
	def createTabbedTextFileFromSearchData(self, dataArrays, fileName):
		"""
		This takes the downloaded and formatted data and create an tabbed file

		@param	dataArrays	(list)	List of Lists of data that will be added to array\
			EX: [ ["Data 1", "Data 2", "Data3"],  ["Data 1", "Data 2", "Data3"]]
		@param	fileName	(str)	Name of the csv file we will write to
		"""
		# This checks to see the filename has already not be created
		if not os.path.isfile(self.base + "/" + fileName ):
			fileToOpen = self.base + "/" + fileName 
		# This will execute if filename already exists
		else:
			# I will be adding Timestamp to FileName Provided to allow for Multiple Files to exist
			# And no file to be overwritten
			fileToOpen = (	self.base + "/" + fileName + 
							datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S") )
		with open(fileToOpen, 'w') as outputFile:
			for dataArray in dataArrays:
				outputFile.write('\t'.join('"{}"'.format(tabbedData) for tabbedData in dataArray) + "\n" )

	def getFileStructure(self, folderToCheck):
		"""
		This Function will check the folderToCheck and provide a list of the files that exist in\
		in the folder in list format to allow the user to parse through.

		@param	str	folderToCheck	The path or folder name to check for files
		"""
		self.log.info("Checking to see how many files exist in {}".format(folderToCheck))
		fileInPath = [os.path.join(folderToCheck, filePath) for filePath in os.listdir(folderToCheck) if os.path.isfile(os.path.join(folderToCheck, filePath))]
		dirInPath =  [dirPath for dirPath in os.listdir(folderToCheck) if os.path.isdir(os.path.join(folderToCheck, dirPath))]
		return fileInPath
	
	def processFile(self, fileName):
		"""
		This function will read the file and remove the first portion of the data and only return information that we expect
		"""
		
		# Line Numbers that are just NewLines
		newLines = []
		myString = ''
		with open(fileName, 'r') as inputFile:
			listOfLines = inputFile.readlines()
			for iterObj, line in enumerate(listOfLines):
				if line == "\n":
					newLines.append(iterObj)
			tempFile = listOfLines[newLines[0]+1:]
			for line in tempFile:
				line.replace("\n", " ")
				myString += line.replace("\n", " ")
		return myString

	def createCSVFromDataFiles(self, fileList):
		"""
		This function will look at a list of files will return a created csv that will include all of the text records from the document
		"""
		tempList = []
		for fileName in fileList:
			tempList.append([fileName, self.processFile(fileName = fileName)])
		
		self.createCSVFromSearchData(	titleList = ['Filename', 'Review'], 
										dataArrays = tempList, 
										fileName = "CSVDBTest")

if __name__ == '__main__':
	# For your own log file to avoid merge conflicts = Name the class something else
	workerClass = Nsgclass(name = "Khuram", logging=True)
	atheism  = workerClass.getFileStructure(folderToCheck= workerClass.base + "/20_newsgroups/alt.atheism")
	workerClass.createCSVFromDataFiles(fileList=atheism)
	"""
	workerClass.createCSVFromSearchData(titleList = ['Critic Name', 'Critic Publication', 'Critic Rating',
													 'Review', 'Date', 'Score', "Fresh Or Rotten"], 
										dataArrays = reviews, 
										fileName = "CSVDB")
	# This will show printed out data format for the returned reviews
	for iterObj, review in enumerate(reviews):
		print("Iter: {}, Review: {}".format(iterObj, review))
	"""
