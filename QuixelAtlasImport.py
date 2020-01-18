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

# 1. Promt User for Library Path
from __future__ import print_function ##to get access to line sep features. print("Foo", "bar", sep= "tauscht das Komma mit Inhalt der Anführungszeichen aus")

while True: #envelope loop
	##Input Assistant:
	print("be careful that you enter following inputs correctly, there is no check for invalid paths. The script is not case sensitive.")
	LibraryPath = raw_input("Enter the path of your Quixel Library Directory (e.g. C:\Data\Quixel Library)")
	SourcePath = raw_input("Enter the path of your source folder containing all texture maps to be imported (e.g. C:\Users\You\Documents\MyAwesomeDecal). If you have a custom preview (1280x1280) as png, put it in this folder named 'preview.png' to make the script use this instead of a generated one.")
	name = raw_input("Enter the name you wish to see in Bridge after import")
	ID = raw_input("Enter the ID you wish to have for your Atlas/Decal. (Tip: use the ID of the source atlas with xy coordinates describing the position of the Decal in the Atlas in terms of rows and columns. rcihc2 ->xyrcihc2 e.g. 24rcihc2")
	mCat = raw_input("Enter the Top-Level Category for your Atlas/Decal, e.g. Asphalt, Brick, Brushes, Bush, Climber,... .")
	sCat = raw_input("Enter the secondary Category for your Atlas/Decal, e.g. for Top Level Asphalt - Coarse, Cracked, Dried, Fine, ...")
	
	## Resolution Chooser. 1,2,4,8 und enter um Auflösung zu wählen.
	resChoose = raw_input("For 1K enter 1, for 2K enter 2, for 4K enter 4, for 8K enter 8.)
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
	scanArea = raw_input("Enter the dimensions of the scanned area. This is meta-data and not vital information. e.g. 2*2, 0.25x0.25 or else.")
	height = raw_input("Enter height of the scanned surface. This is meta-data and not vital information.")
	
	##Enter Tags:
	tags = []
	 while True:
		tmptag = raw_input("You can now enter tags, one at a time, and press enter to accept it. If you are done, enter 'done' to continue with the script.")
		if tmptag != 'done':
			tags.append(tmptag)
		else:
			break
	print("Here you can check if you made any mistakes, and if necessary, restart the assistent.", , "Libary Path: " + LibraryPath, "Source Path: " + SourcePath, "Name: " + name, "ID: " + ID, "Main Category: " + mCat, "Secondary Category: " + sCat, "Resolution: " + resolution, "Scan Area: " + scanArea, "Scan Heigt: " + height, "Tags: " + tags, sep='\n', end='Press Enter to continue...\n')
	##restart assistant logic:
	while True: ##this loop assures that the user has to enter the answer again if it was invalid, and gets a break if a valid answer was given.
	ans = raw_input("Continue? (Y/N)") ##enter answer
		if ans in ("y","Y","n","N"):
			break ## wurde die korrekte Anwort gegeben, wird der while-loop beendet, und das Programm wird fortgesetzt.
		else:
			print("Enter a valid response") # Ist ans etwas anders ans n N y Y, wird der while Loop wiederholt. Solange bis eine korrekte Anwort gegeben wurde.
	### MAIN PROGRAM ###
	
	# 1. Ordner anlegen
	#"$MainCategory"+"_"+"$SubCategory"+"_"+"$ID" (MainCat_SubCat_ID), und darin ein Ordner "previews" und "thumbs/1K & /2K".
	# 2. Source Files umbennen, kopieren und umwandeln (4k zu 1K/2K thumbs)
	
	# 3. 1280x1280 jpg , 360x260 png Preview generieren/kopieren
		#if preview.png in source path rename, 1. pass: sample down to 360x360 and copy to new root, 2. pass: convert 1280x1280 png to jpg and copy to previews folder.
		#else generate preview and copy to new root + previews folder
	# 4. Create new JSON from Template with information filled in.
	# done
	
		