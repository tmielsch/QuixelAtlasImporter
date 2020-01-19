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
import os
import re
import PIL
import json

#from __future__ import print_function ##to get access to line sep features. print("Foo", "bar", sep= "tauscht das Komma mit Inhalt der Anführungszeichen aus")

while True: #envelope loop
	##Input Assistant:
	print("be careful that you enter following inputs correctly, there is no check for invalid paths. The script is not case sensitive. \n")
	LibraryPath = raw_input("Enter the path of your Quixel Library Directory (e.g. C:\Data\Quixel Library) \n")+"\\"
	print("Caution. The script identifies the maps according to matching the first three letters of each name (except two for AO). ALBedo, AO, DISplacement, GLOss, NORmal, OPAcity ROUghness, SPEcular, TRAnslucency. As long these three letters are in the respective file name, the script detects them: \n ")
	SourcePath = raw_input("Enter the path of your source folder containing all texture maps to be imported (e.g. C:\Users\You\Documents\MyAwesomeDecal). If you have a custom preview as png(!), put it in this folder named 'preview.png', to make the script use this instead of a generated one. It will be automatically resizied to 1280x1280/360x360.\n ")+"\\"
	name = raw_input("Enter the name you wish to see in Bridge after import")
	ID = raw_input("Enter the ID you wish to have for your Atlas/Decal. (Tip: use the ID of the source atlas with xy coordinates describing the position of the Decal in the Atlas in terms of rows and columns. rcihc2 ->xyrcihc2 e.g. 24rcihc2): \n ")
	mCat = raw_input("Enter the Top-Level Category for your Atlas/Decal, e.g. Asphalt, Brick, Brushes, Bush, Climber,... .: ")
	sCat = raw_input("Enter the secondary Category for your Atlas/Decal, e.g. for Top Level Asphalt - Coarse, Cracked, Dried, Fine, ...: \n")
	
	## Resolution Chooser. 1,2,4,8 und enter um Auflösung zu wählen.
	resChoose = raw_input("For 1K enter 1, for 2K enter 2, for 4K enter 4, for 8K enter 8.")
	if resChoose == 1:
		print "You entered 1K."
		resolution = "1K"
	elif resChoose == 2:
		print("You entered 2K.")
		resolution = "2K"
	elif resChoose == 4:
		print("You entered 4K.")
		resolution = "4K"
	elif resChoose == 8:
		print("You entered 8K.")
		resolution = "8K"
	else :
		print("Please enter a valid number.")
	##MetaData
	scanAreaVar = raw_input("Enter the dimensions of the scanned area. This is meta-data and not vital information. e.g. 2x2, 0.25x0.25 etc. Formatting is important.")
	height = raw_input("Enter height of the scanned surface. This is meta-data and not vital information.")
	
	##Enter Tags:
	tags = []
	 while True:
		tmptag = raw_input("You can now enter tags, one at a time, and press enter to accept it. If you are done, enter 'done' to continue with the script. \n")
		if tmptag != 'done':
			tags.append(tmptag)
		else:
			break
	print("Here you can check if you made any mistakes, and if necessary, restart the assistent.","", "Libary Path: " + LibraryPath, "Source Path: " + SourcePath, "Name: " + name, "ID: " + ID, "Main Category: " + mCat, "Secondary Category: " + sCat, "Resolution: " + resolution, "Scan Area: " + scanArea, "Scan Heigt: " + height, "Tags: " + tags, sep='\n', end='Press Enter to continue...\n')
	raw_input()#holds the program until enter is pressed.
	##restart assistant logic:
	while True: ##this loop assures that the user has to enter the answer again if it was invalid, and gets a break if a valid answer was given.
	ans = raw_input("Continue? (Y/N): ") ##enter answer
		if ans in ("y","Y","n","N"):
			break ## wurde die korrekte Anwort gegeben, wird der while-loop beendet, und das Programm wird fortgesetzt.
		else:
			print("Enter a valid response") # Ist ans etwas anders ans n N y Y, wird der while Loop wiederholt. Solange bis eine korrekte Anwort gegeben wurde.
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
		raw_input("Failed to create directories. Press Enter to restart assistent. ")
		continue ##restarts the envelope loop
	else: #continue with rest of program
	#read source files
		mapAbr = ["alb","AO","dis","glo","nor","opa","rou","spe","tra"] # patterns for regex
		mapNames = ["Albedo","AO","Displacement","Gloss","Normal","Opacity","Roughness","Specular","Translucency"] # actual names in same order. mapAbr[0]="alb", mapNames[0]= "Albedo"
		SourceNames = os.listdir(SourcePath) # generates array with filenames within the given directory. Isn't necessarily as long as the map-Arrays.
		filenames=[]
		for SourceName in SourceNames:
			#fileName, fileExtension = os.path.splitext(SourcePath+SourceName) obsolete since Image.open opens all images and can convert all types to all types. So no need to check for jpg necessary anymore.
			
			for i, item in enumerate(MapAbr): #check each abbrivation and if one matches do body of if
				if re.match(item, SourceName, flags= re.I): # if item in MapAbr (e.g. "alb") matches with SourceName in Sourcenames, execute body.
					newName=ID+"_"+resolution+"_"+mapNames[i]+".jpg" ## generates the new name for the file based on Type, Resolution and ID.
					img = Image.open(SourcePath+"\\"+SourceName) ##reads in image format independently
					img.save(rootDir+newName)##saves that image with appropriate name and format
					filenames.append(newName+"\n")##fills array with created file names to give user feedback.
				elif re.match(preview.png, SourceName, flags=re.I): #check if a file of the source dir is named previews.png
					preview = Image.open(SourcePath+SourceName)
					print("Preview File found\n")
						
				else:
					print(SourceName+" could't be intentified")
		print("The following files were created based on source input:\n"+filenames
		
		##Previews
		# check if preview was given
		if preview:
			preview.resize((1280,1280),PIL.Image.ANTIALIAS)
			preview.save(rootDir+"previews\\"+ID+"_Preview_Retina_sp.jpg")
			preview.resize((360,360),PIL.Image.ANTIALIAS)
			preview.save(rootDir+ID+"_Preview.png")
		else:
			#1. generate Preview
			alpha = Image.new("RGBA",(1280,1280),(0,0,0,1)) #1.1 generate Alpha-Layer
			alb = Image.open(rootDir+ID+"_"+resolution+"_Albedo.jpg")#1.2 load albedo
			AO = Image.open(rootDir+ID+"_"+resolution+"_AO.jpg") #1.3 load AO
			mask = Image.open(rootDir+ID+"_"+resolution+"_Opacity.jpg") #1.4 Load Opacity Mask
			blended = PIL.ImageChops.multiply(alb, AO)#1.4 Multiply AO with Albedo to get somewhat representative result
			resized = blended.resize((1280,1280),PIL.Image.ANTIALIAS)#1.5resize for 1280x1280 preview in previews dir
			masked = Image.composite(blended, alpha, mask) # 1.6 create alpha masked image
			masked.save(rootDir+"previews\\"+ID+"_Preview_Retina_sp.jpg")#save as jpeg in previews dir
			masked.resize((360,360), PIL.Image.ANTIALIAS)#resize for 36x360 png preview
			masked.save(rootDir+ID+"_Preview.png")# save 360 preview
			print("The previews were generated by blending Albedo and AO with multiply. They are not representative of how the Atlas looks in a PBR engine.\n")
		
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
			maps[item]= Image.open(rootDir+ID+"_"+resolution+"_"+mapNames[i]+".jpg")
			maps[item]= maps[item].resize((2048,2048),PIL.Image.ANTIALIAS)
			maps[item].save(rootDir+"thumbs\\2K\\"+mapNames[i]+".jpg")
			maps[item]= maps[item].resize((1024,1024),PIL.Image.ANTIALIAS)
			maps[item].save(rootDir+"thumbs\\1K\\"+mapNames[i]+".jpg")
			
		#JSON Editing
		
		#1. read json template from home-dir of script
		#2. replace "tmpID" with ID
		#3. replace "tmp_Name" with Name
		#4.	replace "mCat" with mCat
		#5.	replace "sCat" with sCat
		#6 replace "scanAreaVar" with scanArea
		#7 replace "heightVar" with height
				
		# add tags with json 
			
	
	
	
	# 3. 1280x1280 jpg , 360x260 png Preview generieren/kopieren
		#if preview.png in source path rename, 1. pass: sample down to 360x360 and copy to new root, 2. pass: convert 1280x1280 png to jpg and copy to previews folder.
		#else generate preview and copy to new root + previews folder
	# 4. Create new JSON from Template with information filled in.
	# done
	
		
