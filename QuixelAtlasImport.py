##Initialize
#Global Variables

#LibraryPath = PathDummy 
#SourcePath = sPathDummy
#ID = IDdummy
#MainCat = MainCatDummy
#SecCat = SecCatDummy
#Name = NameDummy #für Bridge
#Resolution = ResDummy
#ScanArea = ScanAreaDummy
#tags = []
# ""/'' can be used interchangably but the other has to be used if one is part of the string that is getting defined.

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

# 1. Promt User for Library Path
import os, re, PIL, json, fileinput, sys
from PIL import Image
from shutil import copyfile
#from __future__ import print_function ##to get access to line sep features. print("Foo", "bar", sep= "tauscht das Komma mit Inhalt der Anführungszeichen aus")
prevcheck=0
while True: #envelope loop
	##Input Assistant:
	print("be careful that you enter following inputs correctly, there is no check for invalid paths. The script is not case sensitive. \n")
	LibraryPath = input("Enter the path of your Quixel Library Directory (e.g. C:\\Data\\Quixel Library) \n")+"\\"
	print("Caution. The script identifies the maps according to matching the first three letters of each name (except two for AO). ALBedo, AO, DISplacement, GLOss, NORmal, OPAcity ROUghness, SPEcular, TRAnslucency. As long these three letters are in the respective file name, the script detects them: \n ")
	SourcePath = input("Enter the path of your source folder containing all texture maps to be imported (e.g. C:\\Users\You\\Documents\\MyAwesomeDecal). If you have a custom preview as png(!), put it in this folder named 'preview.png', to make the script use this instead of a generated one. It will be automatically resizied to 1280x1280/360x360.\n")+"\\"
	name = input("Enter the name you wish to see in Bridge after import:\n")
	ID = input("Enter the ID you wish to have for your Atlas/Decal. (Tip: use the ID of the source atlas with xy coordinates describing the position of the Decal in the Atlas in terms of rows and columns. rcihc2 ->xyrcihc2 e.g. 24rcihc2): \n")
	IDminus2 = ID[:-1]
	mCat = input("Enter the Top-Level Category for your Atlas/Decal, e.g. Asphalt, Brick, Brushes, Bush, Climber,... .:\n")
	sCat = input("Enter the secondary Category for your Atlas/Decal, e.g. for Top Level Asphalt - Coarse, Cracked, Dried, Fine, ...: \n")
	
	## Resolution Chooser. 1,2,4,8 und enter um Auflösung zu wählen.
	resChoose = input("For 1K enter 1, for 2K enter 2, for 4K enter 4, for 8K enter 8.\n")
	if resChoose == "1":
		print ("You entered 1K.")
		resolution = "1K"
	elif resChoose == "2":
		print("You entered 2K.")
		resolution = "2K"
	elif resChoose == "4":
		print("You entered 4K.")
		resolution = "4K"
	elif resChoose == "8":
		print("You entered 8K.")
		resolution = "8K"
	else :
		print("Please enter a valid number.")
	##MetaData
	scanAreaVar = input("Enter the dimensions of the scanned area. This is meta-data and not vital information. e.g. 2x2, 0.25x0.25 etc. Formatting is important.\n")
	heightVar = input("Enter height of the scanned surface. This is meta-data and not vital information.\n")
	
	##Enter Tags:
	tagsIn = []
	while True:
		tmptag = input("You can now enter tags, one at a time, and press enter to accept it. If you are done, enter 'done' to continue with the script. \n")
		if tmptag != 'done':
			tagsIn.append(tmptag)
		else:
			break
	print("Here you can check if you made any mistakes, and if necessary, restart the assistent.")
	print("Libary Path: " + LibraryPath)
	print("Source Path: " + SourcePath)
	print("Name: " + name)
	print("ID: " + ID)
	print("Main Category: " + mCat)
	print("Secondary Category: " + sCat)
	print("Resolution: " + resolution)
	print("Scan Area: " + scanAreaVar)
	print("Scan Heigt: " + heightVar)
	print("Tags: ")
	print(tagsIn)
	print("Press Enter to continue or re-run the script if you find an error")
	input()#holds the program until enter is pressed.
	##restart assistant logic:
	#while True: ##this loop assures that the user has to enter the answer again if it was invalid, and gets a break if a valid answer was given.
	#	ans = input("Continue? (Y/N): ") ##enter answer
	#	if ans in ("y","Y","n","N"):
	#		break ## wurde die korrekte Anwort gegeben, wird der while-loop beendet, und das Programm wird fortgesetzt.
	#	else:
	#		print("Enter a valid response") # Ist ans etwas anders ans n N y Y, wird der while Loop wiederholt. Solange bis eine korrekte Anwort gegeben wurde.
	### MAIN PROGRAM ###
	
	# 1. Ordner anlegen
	#"$MainCategory"+"_"+"$SubCategory"+"_"+"$ID" (MainCat_SubCat_ID), und darin ein Ordner "previews" und "thumbs/1K & /2K".
	# 2. Source Files umbennen, kopieren und umwandeln (4k zu 1K/2K thumbs)
		#use regex to identify source files and rename them
		#1. regex alb to ID+"_"+resolution+"_Albedo.jpg" & check if jpg
		#2. regex AO to ID+"_"+resolution+"_AO.jpg" & check if jpg
		#3. usw.
		
	#Create Directories
	rootDir = LibraryPath + "Custom\\atlas\\" + mCat+"_"+sCat+"_"+ID+"\\" ## Generate path name for root directory
	try:
		os.mkdir(rootDir) ##create atlas root folder
		os.mkdir(rootDir +"previews")
		os.mkdir(rootDir +"Thumbs")
		os.mkdir(rootDir+"Thumbs\\1K")
		os.mkdir(rootDir+"Thumbs\\2K")
	except:
		input("Failed to create directories. Check your permissions and rerun assistant.")
		#continue ##restarts the envelope loop
	else: #continue with rest of program
	#read & save source files
		mapAbr = ["alb","AO","dis","glo","nor","opa","rou","spe","tra"] # patterns for regex
		mapNames = ["Albedo","AO","Displacement","Gloss","Normal","Opacity","Roughness","Specular","Translucency"] # actual names in same order. mapAbr[0]="alb", mapNames[0]= "Albedo"
		SourceNames = os.listdir(SourcePath) # generates array with filenames within the given directory. Isn't necessarily as long as the map-Arrays.
		filenames=[]
		for SourceName in SourceNames:
			for i, item in enumerate(mapAbr):
				if re.search(item, SourceName, flags= re.I):
					newName=IDminus2+"_"+resolution+"_"+mapNames[i]+".jpg"
					img = Image.open(SourcePath+SourceName)
					img.save(rootDir+newName)
			filenames.append(newName)
			if re.search("preview.png", SourceName, flags=re.I):
				preview = Image.open(SourcePath+SourceName)
				print("Preview File found\n")
				prevcheck=1
		if prevcheck == 0:
			print("No Preview found. One will be generated instead")
			
	
		print("The following maps were created based on source input:\n")
		print(filenames)
		
		##Previews
		# check if preview was given
		if prevcheck == 1:
			prev1280 = preview.resize((1280,1280),PIL.Image.ANTIALIAS)
			prev1280.save(rootDir+"previews\\"+IDminus2+"_Preview_Retina_sp.jpg")
			prev360 = preview.resize((360,360),PIL.Image.ANTIALIAS)
			prev360.save(rootDir+IDminus2+"_Preview.png")
		else:
			#1. generate Preview
			alb = Image.open(rootDir+IDminus2+"_"+resolution+"_Albedo.jpg").convert("RGBA")#1.2 load albedo
			AO = Image.open(rootDir+IDminus2+"_"+resolution+"_AO.jpg").convert("RGBA") #1.3 load AO
			mask = Image.open(rootDir+IDminus2+"_"+resolution+"_Opacity.jpg").convert("L") #1.4 Load Opacity Mask
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
		
		##Thumbs
		#Load Images
		#alb = Image.open(rootDir+ID+"_"+resolution+"_Albedo.jpg")
		#AO = Image.open(rootDir+ID+"_"+resolution+"_AO.jpg")
		#dis = Image.open(rootDir+ID+"_"+resolution+"_Displacement.jpg")
		#glo = Image.open(rootDir+ID+"_"+resolution+"_Gloss.jpg")
		#nor = Image.open(rootDir+ID+"_"+resolution+"_Normal.jpg")
		#opa = Image.open(rootDir+ID+"_"+resolution+"_Opacity.jpg")
		#rou = Image.open(rootDir+ID+"_"+resolution+"_Roughness.jpg")
		#spe = Image.open(rootDir+ID+"_"+resolution+"_Specular.jpg")
		#tra = Image.open(rootDir+ID+"_"+resolution+"_Translucency.jpg")
		
		#create dict with key = image, resize them and save them accordingly
		maps={}
		for i,item in enumerate(mapAbr):
			maps[item]= Image.open(rootDir+IDminus2+"_"+resolution+"_"+mapNames[i]+".jpg")
			maps[item]= maps[item].resize((2048,2048),PIL.Image.ANTIALIAS)
			maps[item].save(rootDir+"thumbs\\2K\\"+IDminus2+"_2K_"+mapNames[i]+".jpg")
			maps[item]= maps[item].resize((1024,1024),PIL.Image.ANTIALIAS)
			maps[item].save(rootDir+"thumbs\\1K\\"+IDminus2+"_1K_"+mapNames[i]+".jpg")
			
		#JSON Editing
		
		#1. copy template json to rootDir
		templatepath = os.path.join(sys.path[0], "template.JSON")
		copyfile(templatepath, rootDir+ID+".json")
		#2.replace alll "ID". The ID for atlasses has a "2" added after the ID for the name of the JSON file, as well as the directory name. The maps miss this appendix.
		#with line.replace every part of a string matching the pattern-string gets replaced. Since it's "id:tmpID2" in the file, just the tmpID portion gets replaced.
		
		
				
		#Serialize JSON
		#the rest of the data in the JSON has to be replaced with regex to avoid unwanted replacements. (Regex supports whole-word search and replace)
		with fileinput.FileInput(os.path.join(rootDir, ID+".json"), inplace=True, backup =".bak") as f:
			for line in f:
				print(line.replace("tmpID", IDminus2), end='')
		
		with open(os.path.join(rootDir, ID+".json"), "r") as J: # opens .json as J
			match={r"\btmpName\b":name,r"\bmCat\b":mCat,r"\bsCat\b":sCat,r"\bscanAreaVar\b":scanAreaVar,r"\bheightVar\b":heightVar}#{pattern:replacestring}
			def replace_all(text,dic):
				for key, val in dic.items():
					text = re.sub(key,val,text)
				return text
			
			
			jdict = json.load(J) # serializes the content of the loaded json as "jcontent" (type dict)
			jdict['tags'] = tagsIn
			jstring = json.dumps(jdict, indent=4) # dumps the content into a single string
			jstring = replace_all(jstring,match) #replaces all keyWords in the jstring with the Variable Values
			#jredict = json.loads(jstring) # isn't necessary.
			
			##tags
			
			
			
			
			with open(os.path.join(rootDir, ID+".json"),"w") as savefile:
				#json.dump(jredict, savefile)#dumps the modified string back into the json file.
				savefile.write(jstring)#Writes the human-readable string to file
			
			
			
			
		###tags	
			
		
		
		
		
		#Done?
		break	
			
		
		# add tags-array with json 
		
		#copy and rename template.json into rootDir
		#print("Import complete. The atlas should now show up under the "mixer" category")
			
	
	
	
	# 3. 1280x1280 jpg , 360x260 png Preview generieren/kopieren
		#if preview.png in source path rename, 1. pass: sample down to 360x360 and copy to new root, 2. pass: convert 1280x1280 png to jpg and copy to previews folder.
		#else generate preview and copy to new root + previews folder
	# 4. Create new JSON from Template with information filled in.
	# done
	
		
