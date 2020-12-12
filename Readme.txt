Syntax to Run program:
	python3 fileID.py  :This will categorize files in the current Working Directory

	python3 fileId.py -i [File name]   :To identify type of a single file
	
	python3 fileID.py -t [Address to text file]   :This will read filenames from text file in address provided

	python3 fileID.py -f [Address to folder]   :This will read filenames from folder in address provided  

Expected output:
	Categorized list of files is displayed, and is also written to file 'categorizedList.txt'
	

Optional:
	python3 updateDB.py  : This script will check online for new extensions and update the database if any new extensions are found  



Contents:
	fileID.py  	: Main program to be run
	categorizer.py  : Scrpit is used by fileID.py to identify and categorize files
	extensions.db   : Database where information about filetypes are stored
	updateDB.py	: Script to scrape data from internet and update database(Can be run based on user preference)
	categorizedList.txt : Output is written to this file after each execution
	sample.txt	: Sample input file with random file names

	scrapper.py	: The script that was used for creating database(For evaluation purpose only)
		
	
