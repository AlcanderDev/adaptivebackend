import requests
import re
from xml.etree import cElementTree as ET

# Reads configuration file and store them into a dictionary
def ReadConfig(dirName, config):
	for line in open(dirName, 'r'):
		line = re.sub(r"[\n\t\s]*", "", line)
		idx = line.find(':')
		config[line[:idx]] = line[idx+1:]

# Encodes all special characters into usable URL form for wolframalpha
def WolframUrlEncode(input, specDict):
	# Remove all whitespaces
	input = input.replace(" ", "")
	# Encode all required characters
	for key, value in specDict.iteritems():
		input = input.replace(key, value)
	return input

def RetrieveStepByStep(rawOutput, config):
	# We will retrieve the entire contents of <plaintext>
	# Go to the step portion
	rawOutput = rawOutput[rawOutput.find(config["start"]):]
	start = rawOutput.find(config["openStep"])
	end = rawOutput.find(config["closeStep"])
	stepbystep = rawOutput[start+len(config["openStep"]):end]
	return stepbystep

# This function MUST take in raw string in order to process the \ character as raw form
def WolframQueryForStepByStep(input, config, appKey):
	appID = appKey["key"]
	input = WolframUrlEncode(input, config)
	url = 'http://api.wolframalpha.com/v2/query?appid='+ appID +'&input=solve+' + input + '&podstate=Step-by-step%20solution&includepodid=Result'
	response = requests.post(url)
	response = unicode(response.text).encode('utf8')
	#print(response)
	return RetrieveStepByStep(response, config)
	
# This function quantifies the percentage of each steps
def QuantifyStepsPercentages(input, stepsDict):
	PercentageDict = dict()
	totalAmt = 0
	for key, value in stepsDict.iteritems():
		amt = input.count(key)
		totalAmt = totalAmt + amt
		PercentageDict[value] = amt
	# Compute Actual Percentages
	for type, occurence in PercentageDict.iteritems():
		if(totalAmt==0):
			print("Error: No solutions for " + input)
			return PercentageDict
		PercentageDict[type] = (float(occurence) / totalAmt) * 100
	return PercentageDict
	
# This function combines both query and quantifying percentages
def WolframGetPercentage(input, config, stepsDict):
	return QuantifyStepsPercentages(WolframQueryForStepByStep(input, config), stepsDict)

# Init Function
def WolframInit(config, stepsDict):
	ReadConfig("encode.dat", config)
	ReadConfig("stepsDict.dat", stepsDict)

# Test Function
def Test():
	# Read encoding dict
	config = dict()
	stepsDict = dict()
	appKeyDict = dict()
	ReadConfig("encode.dat", config)
	ReadConfig("stepsDict.dat", stepsDict)
	ReadConfig("appKey.dat", appKeyDict)
	print(QuantifyStepsPercentages(WolframQueryForStepByStep(r"\frac { 4 } { 9 } p ^ { 2 } + p - 1", config, appKeyDict), stepsDict))
	
#Test()


