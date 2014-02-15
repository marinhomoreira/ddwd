import xmltodict, json, sys, codecs, re, glob, shutil, os

'''
command: python xmlToJson.py <root/path/with/xml/files> <path/to/master/files/folder>
example: python xmlToJson.py ~/Desktop/ianode/ImagineCup/test ~/Desktop/ianode/ImagineCup/masterfiles

Never tested on windows. Made for linux. Penguin ftw!

Process:
1. Creates masterfile (generateMasterFile(globPath)
2. Remove <xml> tags and NUL characters (cleanXML(filename)) from each file from the directory passed as arg1
3. Add the content of each file generated in 2 to master file
4. Finalize master file (puts tag </tweets> and closes the file)
5. Generates .json file from each .xml master.
'''

def main():
	rootPath = sys.argv[1]
	mastersPath = sys.argv[2]
	#fileType is related to file filter. e.g. "*.xml" is defined, glob will look only for .xml files. Hardcoded now.
	#fileType = sys.argv[3] 
	fileType = ""
	generateMasters(rootPath, fileType, mastersPath)

def generateMasterFile(root, dir, masterPath):
	globPath = os.path.join(root, dir) + "/*.xml" # looks only for *.xml files in the directory
	files = glob.glob(globPath)
	if len(files) != 0:
		# master xml filename is named after the directory of the files
		master = os.path.join(masterPath, dir) + "-Master.xml"
		print "Creating " + os.path.basename(master)
		initializeMasterXml(master)
		for file in files:
			addContentToMasterFile(master, cleanXML(file))
		# add last tag
		finalizeMasterXml(master)
		generateJSON(master)
		# TODO: clean the garbage (aka temp/dummy files)
	else:
		print "Couldn't find any valid files on "+dir

def cleanXML(filename):
	# remove tags <xml> and NUL characters
	original = open(filename)
	tempFilename = filename+".temp"
	xmlParsedFile = open(tempFilename, "wb")
	for line in original:
		line = line.replace("<xml>","")
		line = line.replace("</xml>","")
		line = line.replace('\0','')
		xmlParsedFile.write(line)
	original.close()
	xmlParsedFile.close()
	return tempFilename

def addContentToMasterFile(master, fileToBeAddedToMaster):
	destination = open(master, 'a')
	origin = open(fileToBeAddedToMaster, 'r')
	shutil.copyfileobj(origin, destination)
	origin.close()
	destination.close()
	
def initializeMasterXml(master):
	# add first tag <tweet>
	master = open(master, 'w')
	master.write('<tweets>\n')
	master.close()
	
def finalizeMasterXml(master):
	# add last tag </tweet>
	master = open(master, 'a')
	master.write('\n</tweets>')
	master.close()
	
def generateJSON(masterFilename):
	jsonFilename = masterFilename.replace('.xml', '.json.temp') # workaround to perform the gambigambi operation and come up with the real final json
	fileIn = open(masterFilename, 'rb')
	fileOut = codecs.open(jsonFilename, encoding='utf-8', mode='w+')
	try:
		o = xmltodict.parse(fileIn)
		fileOut.writelines(json.dumps(o, ensure_ascii=False))
	except:
		print "HOUSTON, we have a problem with file " + masterFilename
		pass
	else:
		fileIn.close()
		fileOut.close()
		GambiGambi(jsonFilename)
	fileIn.close()
	fileOut.close()

	# XGH session
	# I'm not proud of it, but it works.
def GambiGambi(jsonFilenameTemp):
	jsonFilename = jsonFilenameTemp.replace('.json.temp','.json')
	fileIn = codecs.open(jsonFilenameTemp, encoding='utf-8', mode='r')
	fileOut = codecs.open(jsonFilename, encoding='utf-8', mode='w+')
	for line in fileIn:
		line = line.replace("{\"tweets\": {\"tweet\": [","")
		line = line.replace("}}]}}","}}")
		line = line.replace(", {\"text\":","\n{\"text\":")
		fileOut.writelines(line)
	fileIn.close()
	fileOut.close()
	print "Creating " + os.path.basename(jsonFilename)

def generateMasters(rootPath, fileType, mastersPath):
	for root, dirs, files in os.walk(rootPath):
		for dir in dirs:
			if os.path.join(root, dir) != mastersPath:
				print "Inside folder " + dir + " now"
				generateMasterFile(root, dir, mastersPath) # add fileType if you want to make it dynamic.
				print ""
# LET THE CARNAGE BEGIN!
main()