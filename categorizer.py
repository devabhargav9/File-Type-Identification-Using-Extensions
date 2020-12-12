# categorizer.py
import sqlite3
import os.path


def getExtension(fileName):
    fileName = fileName.split('.')
    l = len(fileName)
    if (l == 1):  # If filename doesn't have extension
        return None
    else:
        return fileName[l - 1]


def formatCategory(catName):  #Format category name for output 
    catName = catName.capitalize()
    catName = catName.replace('-', ' ')
    return catName + ':'


def categorize(files):
    currentDirectory = os.getcwd()
    pathToDB = os.path.join(currentDirectory, 'extensions.db')  # Create path to database
    database = sqlite3.connect(pathToDB)  # Connect to database
    cur = database.cursor()  # Create cursor
    baseQuery = "SELECT * FROM Extensions WHERE Name = '"
    descriptions = []  # Buffer(list) for storing description for each file
    categories = {}  # Buffer(dictionary) for storing categories and files
    filesCount = len(files)

    for i in range(filesCount):
        extName = getExtension(files[i])  # Get extension from filename

        if (extName):  # If file has a extension
            query = baseQuery + extName + "';"  # Create query for the extension
            try:
                extObj = cur.execute(query)  # Execute query on database
            except:
                print("Unable to retrive data from database!")
                exit(1)
            extInfo = extObj.fetchone()  # Fetch output for the query

            if (extInfo):  # If extension information is found in database
                descriptions.append(extInfo[1])
                category = formatCategory(extInfo[2])
            else:
                descriptions.append("The filetype could not be identified")
                category = "Unidentified File(s):"

        else:
            descriptions.append("File has no Extension")
            category = "Unidentified File(s):"

        if category in categories.keys():  # If category is already in buffer append index of file
            categories[category].append(i)  # that is being checked to the buffer
        else:
            categories[category] = [i]  # Else create a dictionary item for that category

    if (filesCount == 1):  # If only one file is being checked
        print("{0}: {1}".format(files[0], descriptions[0]))
        exit(0)

    outputFile = open('categorizedList.txt', 'w')  # Open output file in write mode
    
    for category in categories.keys():
        print(category)  # Print category title
        outputFile.write(category + "\n")
        for index in categories[category]:  # Print all files it's description under that category
            fileInfo = "\t{0}\t\t{1}".format(files[index], descriptions[index])
            print(fileInfo)
            outputFile.writelines(fileInfo + "\n")  # Write file information to output file
        print()
    
    print("The output is also written to file 'categorizedList.txt'")
    cur.close()  # Terminate connection to database
    database.close()
