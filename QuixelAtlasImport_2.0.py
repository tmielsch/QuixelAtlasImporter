# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import os, re, PIL, json, fileinput, sys
from PIL import Image
from shutil import copyfile

#global Variables
prevcheck = 0

libDir = ""
rootDir = ""

##uIn1:
uIn1={srcDir
srcDir = ""
mCat = ""
sCat = ""
res = ""
scnA = ""
scnH = ""
tagsIn = []
data = {} ##contains json serialization


# Function Declarations
#TODO Add save logic to uIn1() & uInLib()
#uInput
def uInLib():#handles just the library input
	libDir = input("Enter the path of your Quixel Library Directory (e.g. C:\\Data\\Quixel Library) \n")+"\\"
	##add save logic
def libDirR():#reads libDir from data, calls uInLib if it can't find any stored, and asks if user wants to change stored
	if data['libDir'] == "": ##check if there is no stored libDir in data
		uInLib() ## if not, ask for it and save it to data.json
	elif data['libDir'] != "":
		print("This is your stored library directory: "+data['libDir'])
		switch = input('Press enter to continue without changes, or type anything and confirm to change the library directory.')
		if switch == "":
			libDir = data['libDir']##if user pressed enter, just use the stored libDir as libDir. Don't change the file.
		if switch != "":#if user entered some string, reask for libDir
			uInLib() ##uInLib is called to set libDir and save it to data.json
def uIn0(): ## This function handles uInput that has to be made each time. // Has to be called in every iteration
	print("Be careful, there is no check for invalid paths.\n")
	print("Make sure your maps have at least the three first letters in their Abbrevation. e.g. mapname_alb.jpg (except AO)."
	srcDir = input("Enter the path of your source folder containing all texture maps to be imported. You can provide your custom preview named as such to avoid a generated one.: ")
	name = input("Enter the name visible in Bridge: ")
	ID = input("Enter an ID. (Tip: use the ID of the source atlas with xy coordinates describing the position of the Decal in the Atlas in terms of rows and columns. rcihc2 ->xyrcihc2 e.g. 24rcihc2): ")
	IDminus2 = ID[:-1] ## removes the "2" from the name for naming the maps in the rootDir
def uIn1(): ## This function handles uInput that can be reused in further iterations (like category, tags, height, scan size etc.) //has to be called only when neccesarry.
	mCat = input("Enter the Top-Level Category for your Atlas/Decal, e.g. Asphalt, Brick, Brushes, Bush, Climber,... .:\n")
	sCat = input("Enter the secondary Category for your Atlas/Decal, e.g. for Top Level Asphalt - Coarse, Cracked, Dried, Fine, ...: \n")
	## res Chooser. 1,2,4,8 und enter um Auflösung zu wählen.
	resChoose = input("For 1K enter 1, for 2K enter 2, for 4K enter 4, for 8K enter 8.\n")
	if resChoose == "1":
		print ("You entered 1K.")
		res = "1K"
	elif resChoose == "2":
		print("You entered 2K.")
		res = "2K"
	elif resChoose == "4":
		print("You entered 4K.")
		res = "4K"
	elif resChoose == "8":
		print("You entered 8K.")
		res = "8K"
	else :
		print("Please enter a valid number.")
	##MetaData
	scnA = input("Enter the dimensions of the scanned area. This is meta-data and not vital information. e.g. 2x2, 0.25x0.25 etc. Formatting is important.\n")
	scnH = input("Enter height of the scanned surface. This is meta-data and not vital information.\n")
	
	##Enter Tags:
	tagsIn = []
	while True:
		tmptag = input("You can now enter tags, one at a time, and press enter to accept it. If you are done, enter 'done' to continue with the script. \n")
		if tmptag != 'done':
			tagsIn.append(tmptag)
		else:
			break
	##########TO ADD############
	###Save variables as JSON###

def uInConfirm(): ##prints all uIn values and stops the program so user can restart or continue
	print("Here you can check if you made any mistakes, and if necessary, restart the assistent.")
	print("Libary Path: " + libDir)
	print("Source Path: " + srcDir)
	print("Name: " + name)
	print("ID: " + ID)
	print("Main Category: " + mCat)
	print("Secondary Category: " + sCat)
	print("res: " + res)
	print("Scan Area: " + scnA)
	print("Scan Heigt: " + heightVar)
	print("Tags: ")
	print(tagsIn)
	print("Press Enter to continue or re-run the script if you find an error")
	input()#holds the program until enter is pressed.

def mkDir(): ## handles directory creation
	#Create Directories
	rootDir = libDir + "Custom\\atlas\\" + mCat+"_"+sCat+"_"+ID+"\\" ## Generate path name for root directory
	try:
		os.mkdir(rootDir) ##create atlas root folder
		os.mkdir(rootDir +"previews")
		os.mkdir(rootDir +"Thumbs")
		os.mkdir(rootDir+"Thumbs\\1K")
		os.mkdir(rootDir+"Thumbs\\2K")
	except:
		input("Failed to create directories.Check permissions and delete previously created directories.")

def cpMaps(): ##handles copying and converting maps from source to root
	mapAbr = ["alb","AO","dis","glo","nor","opa","rou","spe","tra"] # patterns for regex
		mapNames = ["Albedo","AO","Displacement","Gloss","Normal","Opacity","Roughness","Specular","Translucency"] # actual names in same order. mapAbr[0]="alb", mapNames[0]= "Albedo"
		srcNames = os.listdir(srcDir) # generates array with filenames within the given directory. Isn't necessarily as long as the map-Arrays.
		filenames=[]
		for srcName in srcNames:
			for i, item in enumerate(mapAbr):
				if re.search(item, srcName, flags= re.I):
					newName=IDminus2+"_"+res+"_"+mapNames[i]+".jpg"
					img = Image.open(srcDir+srcName)
					img.save(rootDir+newName)
			filenames.append(newName)
			if re.search("preview.png", srcName, flags=re.I):
				preview = Image.open(srcDir+srcName)
				print("Preview File found\n")
				global prevcheck=1
		if prevcheck == 0:
			print("No Preview found. One will be generated instead")
			
	
		print("The following maps were created based on source input:\n")
		print(filenames)	

def prev(): # handles preview generation or conversion

	# check if preview was given
	if prevcheck == 1:
		prev1280 = preview.resize((1280,1280),PIL.Image.ANTIALIAS)
		prev1280.save(rootDir+"previews\\"+IDminus2+"_Preview_Retina_sp.jpg")
		prev360 = preview.resize((360,360),PIL.Image.ANTIALIAS)
		prev360.save(rootDir+IDminus2+"_Preview.png")
	else:
		#1. generate Preview
		alb = Image.open(rootDir+IDminus2+"_"+res+"_Albedo.jpg").convert("RGBA")#1.2 load albedo
		AO = Image.open(rootDir+IDminus2+"_"+res+"_AO.jpg").convert("RGBA") #1.3 load AO
		mask = Image.open(rootDir+IDminus2+"_"+res+"_Opacity.jpg").convert("L") #1.4 Load Opacity Mask
		blended = PIL.ImageChops.multiply(alb, AO)#1.4 Multiply AO with Albedo to get somewhat representative result
		
		#create 360x360 alpha masked png
		alpha = blended.copy()
		alpha.putalpha(mask) # uses Opacity mask to create png preview
		alpha = alpha.resize((360,360))
		alpha.save(rootDir+ID+"_Preview.png")
		#create 1280x1280 JPG
		grey = Image.new("RGB",blended.size, (34,34,34))
		RGB = Image.composite(blended,grey,mask).resize((1280,1280),PIL.Image.ANTIALIAS)
		RGB.save(rootDir+"previews\\"+ID+"_Preview_Retina_sp.jpg")
		
		print("The previews were generated by multiplying Albedo with AO. They are not representative of how the Atlas looks in a PBR engine.\n")	

def thumbs(): ##handles map>thumb conversion
	maps={}
	for i,item in enumerate(mapAbr):
		maps[item]= Image.open(rootDir+IDminus2+"_"+res+"_"+mapNames[i]+".jpg")
		maps[item]= maps[item].resize((2048,2048),PIL.Image.ANTIALIAS)
		maps[item].save(rootDir+"thumbs\\2K\\"+IDminus2+"_2K_"+mapNames[i]+".jpg")
		maps[item]= maps[item].resize((1024,1024),PIL.Image.ANTIALIAS)
		maps[item].save(rootDir+"thumbs\\1K\\"+IDminus2+"_1K_"+mapNames[i]+".jpg")

def jEdit(): ##handles JSON editing
	#copy template to root 
	copyfile(os.path.join(sys.path[0], "template.JSON", rootDir+ID+".json")
	#change tmpID to IDminus2 (for the one case IDwith2(ID), the string is tmpID2, so just the tmpID portion gets replaced, the 2 stays.
	with fileinput.FileInput(os.path.join(rootDir, ID+".json"), inplace=True, backup =".bak") as f:
			for line in f:
				print(line.replace("tmpID", IDminus2), end='')
	
	with open(os.path.join(rootDir, ID+".json"), "r+") as J: # opens .json as J
		##Use dict key as String-to-replace and value as string to replace with.
		match={r"\btmpName\b":name,r"\bmCat\b":mCat,r"\bsCat\b":sCat,r"\bscanAreaVar\b":scnA,r"\bheightVar\b":scnH}#{pattern:replacestring}
		def replace_all(text,dic): #handles the replace all whole words logic
			for key, val in dic.items():
				text = re.sub(key,val,text)
			return text
		jdict = json.load(J) # serializes the content of the loaded json as "jcontent" (type dict)
		jdict['tags'] = tagsIn #adds tags to "tags" key in json
		jstring = json.dumps(jdict, indent=4) # dumps the content into a single string with indentation
		jstring = replace_all(jstring,match) #replaces all keyWords in the jstring with the Variable Values
		J.write(jstring)#Writes the human-readable string to file

def loadData(): #handles loading data.json
	d = open('data.json',"w+")
	data = json.load(d) # serializes data.json as dict (initialized as global var)


	
def uIn1R():#reads uIn1 from file, calls uIn1() if nothing found, and asks if user wants to change them.
	in1keys ={'mCat':mCat,'sCat':sCat,'res':res,'scnA':scnA,'scnH':scnH,'tagsIn':tagsIn}#contains all dict keys to iterate through
	counter = 0
	
	for key, val in in1keys.items():
		if data[key] != "": ##check if data[key] is empty. If not:
			counter += 1
			
	if counter == 0: #if data is empty
		uIn1()#call uIn1 (which promts user input and saves it to file)
	if counter > 0: #if there is data
		switch = input('Shall category, tags, scan area/height and resolution stay the same? If yes, just hit enter, if not, enter something and confirm.: ')
			if switch == "":
				for key, val in in1keys.items():
					key = data[key] #e.g. global var mCat = data['mCat']. Die Frage ist, ob er val auch mit mCat ersetzt - tut er nicht.
					### ich kann alle globalen uIn1 Variablen in einem Dict zusammenfassen. Dann müssen aber alle Referenzen entsprechend ersetzt werden.
				
				
				for key, val in in1keys.items():
					data[key]=val## e.g. 'mCat':mCat
				
					
			
			
			
			
			
			
			
			uInLib() ## if not, ask for it and save it to data.json

#1. is Library path in file?
libDirR() #read libDir from data.json and call uInLib if no data in file

switch = input('Shall category, tags, scan area/height and resolution stay the same? If yes, just hit enter, if not, enter something and confirm. ')
if

	
	
	
#2. are uIn1-Vars in file? If not call uIn1(), if yes load them from file and ask user to confirm
#3. ask for uIn0()
#4. print summary
#5. run routine.


