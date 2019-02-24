#!/usr/bin/env python
import sys
import base64
import requests
import json
import os

# Reads configuration file and store them into a dictionary
def ReadConfig(dirName, config):
	for line in open(dirName, 'r'):
		line = re.sub(r"[\n\t\s]*", "", line)
		idx = line.find(':')
		config[line[:idx]] = line[idx+1:]

def CallAPI(file_path, config):
	user = config["user"]
	key = config["key"]
	image_uri = "data:image/jpg;base64," + base64.b64encode(open(file_path, "rb").read())
	# (python3) image_uri = "data:image/jpg;base64," + base64.b64encode(open(file_path, "rb").read()).decode()
	r = requests.post("https://api.mathpix.com/v3/latex",
		data=json.dumps({'src': image_uri}),
		headers={"app_id": user, "app_key": key,
				"Content-type": "application/json"})
	return json.dumps(json.loads(r.text), indent=4, sort_keys=True)
	
def GetAllDirectoryAndFiles(fileDict, catList, dirName, type = ""):
	# create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
			catList.append(entry)
			GetAllDirectoryAndFiles(fileDict, catList, fullPath, entry)
        else:
			fileDict[fullPath] = (entry, type)               
    return
	
def CreateAllDirectories(catList, dir):
	for cat in catList:
		directory = dir + "\\" + cat
		if not os.path.exists(directory):
			os.makedirs(directory)
	return

# Changes the file extension to .newExt
def ChangeFileExtension(fileName, newExt):
	return fileName[0:fileName.rfind('.')] + newExt
	
def Convert():
	appKeyDict = dict()
	fileDict = dict()
	catList = list()
	# Get a dictionary of all files and the categories
	GetAllDirectoryAndFiles(fileDict, catList, "D:\Git\AdaptiveBackend\Source\Mathplx\Input")
	# Create directories of all categories
	outputDir = "D:\Git\AdaptiveBackend\Source\Mathplx\Output"
	CreateAllDirectories(catList, outputDir)
	ReadConfig("appKey.dat", appKeyDict)

	for question, pair in fileDict.iteritems():
		# Create the json file
		newFileName = ChangeFileExtension(pair[0], ".json")
		file = open(outputDir + "\\" + pair[1] + "\\" + newFileName, "w+")
		file.write(CallAPI(question, appKeyDict))
		file.close()
	return
	
Convert()


