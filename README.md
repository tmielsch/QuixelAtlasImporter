# QuixelAtlasImport
 
Quixel Decal Compiler

https://opensource.com/life/15/2/resize-images-python
https://note.nkmk.me/en/python-pillow-composite/
https://pythontesting.net/python/regex-search-replace-examples/#in_python
https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
https://www.programiz.com/python-programming/file-operation

0. prompt for decal name (z.B. 
1. take maps path
2. take albedo map + AO, multiply them together and mask them using opacity to generate 4k preview
3. generate previews with names based on decalname

Ask new ID
Ask Resolution
Ask Metadata (Name, Category etc.)
Ask Map folder

Beispiel: 
"$id"_4K_Albedo 

id = rcihc11
foldername = moss_atlas_"$id"

Map Names in Files and JSON:

1. Take any map with alb, no, tra, in their name & rename them according to given ID and detected resolution aiwhfaouihwgoauihwg_alb.png at 4096 > ID_4K_Albedo.png
2. Take the ID and add it as a prefix to any albedo(gloss, etc. respectively) reference in the base-JSON. (In the base JSON, instead the ID prefix gets deleted so it's just "$ID"+"_1K/2K/4K/8K_Albedo/Gloss/etc.jpg/.exr"

> So for each of the 9 map types there are 4 Resolution variants (3 if it's only a 4k) in two formats. A total of 72 entries
> there should be a base-JSON for all availible resolutions, or maybe it doesn't matter and one for 8k is enough.
1 Array Map Types = [Albedo,Gloss,Roughness,Translucency,AO,Displacement,Normal,Opacity,Specular]
1 Array Resolutions = [1K,2K,4K,8K] // wenn es keine 
1 Array formats = [".jpg",".exr"]

Nested for loops

for i1, in Map Types
	for i2 in Resolutions
		for i3 in Formats
			replace "$i2_$i1_$i3" with "$ID_$i2_$i1_$i3"
			ignore errors (if 8K missing don't change it) //Ihm ist es ja auch egal wenn es keine 2K texturen gibt - sie stehen trotzdem in der JSON - warum sollte es mit 8K anders sein.


Previews:

Die Preview Datei aus dem Ordner wird nicht direkt referenziert. 
Das einfachste wird es wohl sein 		
			


/////////////////////////////////////

Die Base-JSON bekommt eine PlatzhalterID, die mit der vom Nutzer angegebenen ersetzt wird. Mit ihr werden alle referenzen für previews, maps et.c auf einmal ersetzt. So kann man ein simples search&replace durchführen anstatt selektiv zeilen zu suchen und diese zu ändern.

User Input:

Das Programm fragt am Anfang nach dem Library-Pfad und dem Source-Ordner. Der Source-Ordner enthält einfach nur die maps, die heißen können wie sie wollen, solange sie drei buchstaben des Map-Types enthalten.

Es wird dann nach der gewünschten ID (für Maps+JSON), Name (für Bridge), Kategorien(Einordnung in Bridge+Ordnername), Auflösung(1.1K,2.2K,3.4K,4.8K für Dateinamen), und tags gefragt. Optional kann noch nach der ScanArea und texelDensity gefragt werden. Die Texeldensity ist egal. (Sollte aber in der Doku so angegeben werden), die Scanarea ist bei 4k und 4*4 elementen entsprechend 1k. Die Höhe muss man abschätzen.

Es wird nach einem 1280x1280 png preview file gefragt. Wenn keins angegeben wird, wird die Preview aus AO und Albedo generiert (mal testen was mit anderen maps passiert)

Programm:

>Dann wird ein Ordner in der Library mit dem Namen "$MainCategory"+"_"+"$SubCategory"+"_"+"$ID" angelegt (MainCat_SubCat_ID), und darin ein Ordner "previews" und "thumbs/1K /2K".

>Die Maps aus dem Sourcefolder werden mit neuen Namen basierend auf den Dateinamen und dem Userinput in den Hauptordner kopiert.
(DOKU: Man muss darauf achten dass die Sourcefiles keine Buchstabenfolgen haben, die zu verwechslung führen können.)

>Aus der Albedo und AO Map wird durch Multiply mit einer Maske die preview-Datei erstellt und als "$ID"+"Preview.png" mit 360x360 im Hauptordner, und als "$ID"+"Preview.jpg" mit 1280x1280 im "previews"-Ordner gesichert. Evtl muss für die JPG Datei noch eine Hintergrund Ebene hinzugefügt werden. Also BGLayer+MaskedPNG=JPG.

>Aus den Maps werden nun die thumbs generiert indem sie mit reduzierter Auflösung und entsprechender Änderung des Dateinamens in den entsprechenden Ordnern in "thumbs" gesichert werden.

>Die Template JSON Datei wird eingelesen und basierend auf dem Userinput modifiziert, und wieder als JSON Datei mit "$ID"+".json" gesichert.

Fertig.
















JSON Struktur:

Die JSON Datei besteht aus mehren Objects(PythonDicts, Arrays), die alle nach folgendem Schema strukturiert sind. Keys können modifiziert, hinzugefügt und gelöscht werden.
"object1":{
"key1" : IntVal or "stringVal",
"key2" : IntVal or "stringVal",
"keyX" : IntVal or "stringVal",
},
"object2":{
"key1" : IntVal or "stringVal",
"key2" : IntVal or "stringVal",
"keyX" : IntVal or "stringVal",
},
"object3":{
"index1",
"intex2",
"indexX",
},
...

Map-Dateinnamen:
1. Take any map with alb, no, tra, in their name & rename them according to given ID and detected resolution aiwhfaouihwgoauihwg_alb.png at 4096 > ID_4K_Albedo.png

Die Preview Datei wird aus der Albedo*AO+OpacityMask erzeugt und als "$ID"+"Preview.png" mit einer Auflösung von 360x360px gesichert.
Die Thumbs werden aus den Maps erzeugt. InputMap->InputMap_1k,InputMap_2K und in den jeweiligen Ordnern /Thumbs/1K,2K gesichert.

JSON Modify:

Tags: Die Tags aus der Base-JSON sind gelöscht, so dass das Skript frei neue hinzufügen kann.

1. GoTo Line 3
2. Add Line
3. Enter '"$tagname",'
4. Repeat for as many tags there are in tags[]

//Better

1. JSON Object "tags":[...] to Python Array. tags = [...]
2. add User Input Tags to array
3. PY Array tags =["tag1","tag2",etc] to JSON Object "tags":[]

Meta: Ein Array aus Dicts. i0=scanArea, i1=height, i2=tilable?, i3=texelDensity (resolution of maps //gelogen, 8192 auf 2x2m sind 4k pro meter nicht 8K) der rest ist irrelevant

Categories (Array): i0="atlas" (bleibt da decal), i1="MainCategory(debris e.g.), i2="SubCategory" // Fragt nach Userinput

Extra: Average Color mit ermitteln und ersetzen.



