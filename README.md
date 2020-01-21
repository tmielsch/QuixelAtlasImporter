# QuixelAtlasImporter


1.0 Uses a unstructured program routine without functions or classes. This makes it difficult to modifiy the flow behavior of the program itself.

The aim for 2.0 is, to have a promt "Use settings from last Import?...including tags?" so you just have to enter the changing data like ID and Name while the rest is being remembered.

Optimally, these settings are saved in some sort of json itself so they can be use instead of user input when data is availible. 

1. Ask: Load settings from file?
if yes -> skip all user input saved in file
if no -> ask for user input
	if asked for input, ask: Save settings to file?
continue program

So the program consists of two parts.

Scenarios:
1. User wants to import multiple files with the same underlying data (likely for atlasses) - only ID and Names are changing.
2. User wants du import single file

loop
	0. Library Path initialisation. - save library path always to file, give it as predetermined input so user just has to press enter to accept the path
	1. Variable initialisation based off file or user input, including save to file function
	2. Main Program (Stays unchanged)

Library Path: "Example"?




JSON config file: Stores all uIn0 information permanently.

{
	"libDir":"",
	"mCat":"",
	"sCat":"",
	"res":"",
	"scnA":"",
	"scnH":"",
	"tagsIn":""
}
		
save logic:

the program opens right at the beginning a file "data.json"


Problem: The json gets overwritten in the beginning so that jsom.load has nothing to load.


