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

####global Variables####
dfilename = os.path.join(sys.path[0],'data.json')
prevcheck = 0
preview = "" # contains preview picture opened in cpMaps() to be used by prev()
mapAbr = ["alb","AO","dis","glo","nor","opa","rou","spe","tra"] # patterns for regex
mapNames = ["Albedo","AO","Displacement","Gloss","Normal","Opacity","Roughness","Specular","Translucency"]
libDir = "" #needed throughout the program, set by uInLib()
#Misc Vars
rootDir = ""#needed throughout the program, generated and set by mkDir()
mapNames = [] # created in cpMaps(), needed in thumbs()
data={} # all uIn_R() need to read from data. It's filled by loadData()

##uIn2:
srcDir = ""
name = ""
ID = ""
IDminus2 = ""

##uIn1:
uIn1dict = {'mCat':"",'sCat':"",'res':"",'scnA':"",'scnH':"",'tags':[]} # contains all Variables that can be saved and retrieved to and from JSON
	


# Function Declarations
#TODO Add save logic to uIn1() & uInLib()
#uInput


def loadData(): #handles loading data.json into a dict 'data'
	global data 
	with open(dfilename,"r+") as d:
		data = json.load(d) # serializes data.json as dict (initialized as global var)
	
def saveData(): # handles saving dict 'data' to data.json
	global data
	global d
	os.remove(dfilename) #before data{} can get dumped to data.json, the old json has to be removed to avoid json block after json block getting appended, breaking the json.load()
	with open(dfilename,"w+") as f:
	
		json.dump(data, f, indent=4)
	
def uInLib():#handles just the library input
	global data
	#global libDir
	libDir = input("Enter the path of your Quixel Library Directory (e.g. C:\\Data\\Quixel Library) \n")+"\\"
	data['libDir']=libDir #when uInLib() gets called and the user entered a lib Path, the corresponding key in data gets changed.
	
def InLibR():#reads libDir from data, calls uInLib if it can't find any stored, and asks if user wants to change stored
	global data
	global libDir
	if data['libDir'] == "": ##check if there is no stored libDir in data
		uInLib() ## if not, ask for it and save it to data.json
	elif data['libDir'] != "":
		print("This is your stored library directory: "+data['libDir'])
		switch = input('Press enter to continue without changes, or type anything and confirm to change the library directory.')
		if switch == "":
			libDir = data['libDir']##if user pressed enter, just use the stored libDir as libDir. Don't change the file.
		if switch != "":#if user entered some string, reask for libDir
			uInLib() ##uInLib is called to set libDir and save it to data.json
				
def uIn1(): ## This function handles uInput that can be reused in further iterations (like category, tags, height, scan size etc.) //has to be called only when neccesarry.
	global uIn1dict
	uIn1dict['mCat'] = input("Enter the Top-Level Category for your Atlas/Decal, e.g. Asphalt, Brick, Brushes, Bush, Climber,... .:\n")
	
	uIn1dict['sCat'] = input("Enter the secondary Category for your Atlas/Decal, e.g. for Top Level Asphalt - Coarse, Cracked, Dried, Fine, ...: \n")
	
	## res Chooser. 1,2,4,8 und enter um Auflösung zu wählen.
	resChoose = input("For 1K enter 1, for 2K enter 2, for 4K enter 4, for 8K enter 8.\n")
	
	if resChoose == "1":
		print ("You entered 1K.")
		uIn1dict['res'] = "1K"
		
	elif resChoose == "2":
		print("You entered 2K.")
		uIn1dict['res'] = "2K"
		
	elif resChoose == "4":
		print("You entered 4K.")
		res = "4K"
		
	elif resChoose == "8":
		print("You entered 8K.")
		uIn1dict['res'] = "8K"
		
	else :
		print("Please enter a valid number.")
		
	##MetaData
	
	uIn1dict['scnA'] = input("Enter the dimensions of the scanned area. This is meta-data and not vital information. e.g. 2x2, 0.25x0.25 etc. Formatting is important.\n")
	
	uIn1dict['scnH'] = input("Enter height of the scanned surface. This is meta-data and not vital information.\n")
	
	
	##Enter Tags:
	while True:
		tmptag = input("You can now enter tags, one at a time, and press enter to accept it. If you are done, enter 'done' to continue with the script. \n")
		if tmptag != 'done':
			uIn1dict['tags'].append(tmptag)
		else:
			break
	print(type(uIn1dict))
	#Store promted promted data in data{}
	for key in uIn1dict:
		data[key] = uIn1dict[key]# after all data has been promted and stored in uIn1{}, write this to data{}
		
def In1R():#reads uIn1dict from file, calls uIn1() if nothing found, and asks if user wants to change them.
	in1keys =['mCat','sCat','res','scnA','scnH','tags'] # contains all keys to iterate through
	counter = 0
	global uIn1dict
	global data
	for key in uIn1dict: #take key from uIn1dict (e.g. 'mCat')
		if data[key] != "": ##check if data[key/'mCat'] is empty. If not:
			counter += 1
			
	if counter == 0: #if data is empty
		uIn1()#call uIn1 (which promts user input and saves it to file)
		
	if counter > 0: #if there is data
		switch = input('Shall category, tags, scan area/height and resolution stay the same? If yes, just hit enter, if not, enter something and confirm.: ')
		if switch == "": 				#if pressed enter use file to fill uIn1dict
			for key in uIn1dict:			#uIn1dict is a subset of data. 
				uIn1dict[key] = data[key] 	#Only the keys in uIn1dict are taken from data to fill uIn1dict. e.g. uIn1dict{'mCat':""} = data{'mCat':"override"}
		else:
			uIn1() # call uIn1 to get user Input and write it to file.		

def uIn2(): ## This function handles uInput that has to be made each time. // Has to be called in every iteration
	print("Be careful, there is no check for invalid paths.\n")
	print("Make sure your maps have at least the three first letters in their Abbrevation. e.g. mapname_alb.jpg (except AO).")
	global srcDir
	global name
	global ID
	global IDminus2
	
	srcDir = input("Enter the path of your source folder containing all texture maps to be imported. You can provide your custom preview named as such to avoid a generated one.: ")+"\\"
	
	name = input("Enter the name visible in Bridge: ")
	
	ID = input("Enter an ID. (Tip: use the ID of the source atlas with xy coordinates describing the position of the Decal in the Atlas in terms of rows and columns. rcihc2 ->xyrcihc2 e.g. 24rcihc2): ")
	
	IDminus2 = ID[:-1] ## removes the "2" from the name for naming the maps in the rootDir
					
def uInConfirm(): ##prints all uIn values and stops the program so user can restart or continue
	#global srcDir
	#global name
	#global ID
	#global uIn1dict
	#global libDir
	
	print("Here you can check if you made any mistakes, and if necessary, restart the assistent.")
	print("Libary Path: " + libDir)
	print("Source Path: " + srcDir)
	print("Name: " + name)
	print("ID: " + ID)
	print("Main Category: " + uIn1dict['mCat'])
	print("Secondary Category: " + uIn1dict['sCat'])
	print("res: " + uIn1dict['res'])
	print("Scan Area: " + uIn1dict['scnA'])
	print("Scan Heigt: " + uIn1dict['scnH'])
	print("Tags: ")
	print(uIn1dict['tags'])
	print("Press Enter to continue or re-run the script if you find an error")
	input()#holds the program until enter is pressed.

def mkDirs(): ## handles directory creation
	#Create Directories
	global rootDir
	#global uIn1dict
	rootDir = libDir + "Downloaded\\atlas\\" + uIn1dict['mCat']+"_"+uIn1dict['sCat']+"_"+ID+"\\" ## Generate path name for root directory
	try:
		os.mkdir(rootDir) ##create atlas root folder
		os.mkdir(rootDir +"previews")
		os.mkdir(rootDir +"Thumbs")
		os.mkdir(rootDir+"Thumbs\\1K")
		os.mkdir(rootDir+"Thumbs\\2K")
	except:
		input("Failed to create directories.Check permissions and delete previously created directories.")

def cpMaps(): ##handles copying and converting maps from source to root
	global mapNames
	#global srcDir
	global prevcheck
	global preview
	#global uIn1dict
	mapAbr = ["alb","AO","dis","glo","nor","opa","rou","spe","tra"] # patterns for regex
	mapNames = ["Albedo","AO","Displacement","Gloss","Normal","Opacity","Roughness","Specular","Translucency"] # actual names in same order. mapAbr[0]="alb", mapNames[0]= "Albedo"
	srcNames = os.listdir(srcDir) # generates array with filenames within the given directory. Isn't necessarily as long as the map-Arrays.
	filenames=[]
	for srcName in srcNames:
		for i, item in enumerate(mapAbr):
			if re.search(item, srcName, flags= re.I):
				newName=IDminus2+"_"+uIn1dict['res']+"_"+mapNames[i]+".jpg"
				img = Image.open(srcDir+srcName)
				img.save(rootDir+newName)
		filenames.append(newName)
		if re.search("preview.png", srcName, flags=re.I):
			preview = Image.open(srcDir+srcName)
			print("Preview File found\n")
			prevcheck=1
	if prevcheck == 0:
		print("No Preview found. One will be generated instead")
		

	print("The following maps were created based on source input:\n")
	print(filenames)	

def mkPrev(): # handles preview generation or conversion
	#global uIn1dict
	#global prevcheck
	#global IDminus2
	#global rootDir
	#global ID
	# check if preview was given
	if prevcheck == 1:
		prev1280 = preview.resize((1280,1280),PIL.Image.ANTIALIAS)
		prev1280.save(rootDir+"previews\\"+IDminus2+"_Preview_Retina_sp.jpg")
		prev360 = preview.resize((360,360),PIL.Image.ANTIALIAS)
		prev360.save(rootDir+IDminus2+"_Preview.png")
	else:
		#1. generate Preview
		alb = Image.open(rootDir+IDminus2+"_"+uIn1dict['res']+"_Albedo.jpg").convert("RGBA")#1.2 load albedo
		AO = Image.open(rootDir+IDminus2+"_"+uIn1dict['res']+"_AO.jpg").convert("RGBA") #1.3 load AO
		mask = Image.open(rootDir+IDminus2+"_"+uIn1dict['res']+"_Opacity.jpg").convert("L") #1.4 Load Opacity Mask
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

def mkThumbs(): ##handles map>thumb conversion
	maps={}
	#global rootDir
	#global IDminus2
	#global uIn1dict
	#global mapNames
	for i,item in enumerate(mapAbr):
		maps[item]= Image.open(rootDir+IDminus2+"_"+uIn1dict['res']+"_"+mapNames[i]+".jpg")
		maps[item]= maps[item].resize((2048,2048),PIL.Image.ANTIALIAS)
		maps[item].save(rootDir+"thumbs\\2K\\"+IDminus2+"_2K_"+mapNames[i]+".jpg")
		maps[item]= maps[item].resize((1024,1024),PIL.Image.ANTIALIAS)
		maps[item].save(rootDir+"thumbs\\1K\\"+IDminus2+"_1K_"+mapNames[i]+".jpg")

def jEdit(): ##handles JSON editing
	
	# summary:
	# copies template to rootDir
	# loads the template as jdict
	# modifies the jdict and dumps it into jstring
	# replaces all keywords in the jstring
	# overwrite template file in rootDir with jstring
	
	global name
	#copy template to root 
	templatesrc = os.path.join(sys.path[0], "template.JSON")
	templatetarget = rootDir+ID+".json"
	copyfile(templatesrc, templatetarget)
	
	#change tmpID to IDminus2 (for the one case IDwith2(ID), the string is tmpID2, so just the tmpID portion gets replaced, the 2 stays.
	
	with fileinput.FileInput(os.path.join(rootDir, ID+".json"), inplace=True, backup =".bak") as f:
		for line in f:
			print(line.replace("tmpID", IDminus2), end='')###funktioniert
	
	
	with open(os.path.join(rootDir, ID+".json"), "r+") as J: # opens .json as J
	##Use dict key as String-to-replace and value as string to replace with.
		global name
		global uIn1dict
		#Funktioniert bis auf tmpName - warum auch immer. Es ist die einzige variable die nicht aus uIn1dict geholt wird.
		#heigtVar funktioniert auch nicht?! wtf.
		
		match={r"\btmpName\b":name,r"\bmCat\b":uIn1dict['mCat'],r"\bsCat\b":uIn1dict['sCat'],r"\bscanAreaVar\b":uIn1dict['scnA'],r"\bheightVar\b":uIn1dict['scnH']}#{pattern:replacestring}
		print(match[r"\btmpName\b"])
		print(uIn1dict['tags'])
		
		def replace_all(text,dic): #handles the replace all whole words logic
			for key, val in dic.items():
				text = re.sub(key,val,text)
			return text
		
		jdict = json.load(J) # serializes the content of the loaded json as "jcontent" (type dict)
		jdict['tags'] = uIn1dict['tags'] #adds tags to "tags" key in json
		print(jdict)
		jstring = json.dumps(jdict, indent=4) # dumps the content into a single string with indentation
		print(jstring) ## warum sind hier die tags noch drinnen?!
		jstring = replace_all(jstring,match) #replaces all keyWords in the jstring with the Variable Values
		print(jstring)##hier klappt name auf einmal ?! aber der rest nicht. Als ob es invertiert wäre, und alles was im dump nicht geht, eigentlich gehen sollte und umgekehrt wtf
	
	with open(templatetarget, "w+") as f:
		f.write(jstring)#Writes the human-readable string to file


while True:
#################################LOOP BEGIN#######################################

	#1. With each iteration, data.json gets opened as d to be further used in the program
	
	
	#2. with data.json loaded, it gets deserialized into the data dict. All operations are handled on this dict. After all operations have ended, the dict gets re-serialized into data.json
	loadData()
	
	
	#3. reads libDir from data dict or  call uInLib() to prompt and store libDir into data dict
	InLibR() #libDir=data{'libDir':val}
	
	#4. reads all keys of uIn1dict{} from data{} or call uIn1() to promt and store u1n1{} in data{}
	In1R()
	
	#5. promt user for single-use data
	uIn2()
	
	#6. let user confirm data
	uInConfirm()
	
	##############################################################
	
	#7. create neccessary directories
	mkDirs()
	
	#8. copy and convert maps from source to target
	cpMaps()
	
	#9. generate or convert previews
	mkPrev()
	
	#10. generate thumbs from maps
	mkThumbs()
	
	#11. copy json template and modify it in place
	jEdit()
	
	#12. save data{} to data.json
	saveData()	
#################################LOOP END#########################################
	



