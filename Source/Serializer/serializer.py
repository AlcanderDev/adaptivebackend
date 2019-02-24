import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
import re
from Wolfram import Categorizer

def ReadConfig(dirName, config):
	for line in open(dirName, 'r'):
		line = re.sub(r"[\n\t\s]*", "", line)
		idx = line.find(':')
		config[line[:idx]] = line[idx+1:]
		
def SetDifficultyAndFileList(dictName, config, dirName, type = ""):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            SetDifficultyAndFileList(dictName, config, fullPath, entry)
        else:
			dictName[fullPath] = (type, config[entry[0]])

	
def ReadJSONandSerialize(dictName):
	# Wolfram Init
	wolframConfig = dict()
	wolframStepsDict = dict()
	Categorizer.WolframInit(wolframConfig, wolframStepsDict)
	
	for path, pair in dictName.iteritems():
		with open(path) as f:
			data = json.load(f)
			latex = data["latex"]
			# Solve with Wolfram and get difficulty
			# Get raw string from latex
			percentage = Categorizer.WolframGetPercentage(latex, wolframConfig, wolframStepsDict)
			doc_ref = db.collection(u'secondarytwo').document(latex)
			doc_ref.set({
				u'latex': latex,
				u'type': unicode((pair[0]), "utf-8"),
				u'difficulty': int(pair[1]),
				u'difficultyType': percentage,
			})

# Use the application default credentials
cred = credentials.Certificate('D:/Git/AdaptiveBackend/Source/Serializer/key/adaptivedb-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# Reference Data Adding #
'''
doc_ref = db.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
}
'''

config = dict()
dictList = dict()
ReadConfig("config.dat", config)
SetDifficultyAndFileList(dictList, config, "D:\Git\AdaptiveBackend\Source\Serializer\Input")
ReadJSONandSerialize(dictList)
