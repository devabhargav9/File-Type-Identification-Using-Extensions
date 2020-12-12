import sys
import os
from categorizer import categorize


def invalid():
    print("Invalid usage \n \t fileID.py -f [folder address] to read from folder")
    print("\t fileId.py -t [text file address] to read from a text file")
    print("\t fileId.py -i [File name] to check type of a single file\n")
    exit(1)


def openFolder(path):
    try:
        content = os.listdir(path)  # Get a list of files in given given folder
    except:
        print("Folder Path invalid!")
        exit(1)
    if (len(content) == 0):
        print("The folder is empty!")  # If the folder is empty
        exit(0)
    categorize(content)


def openText(path):
    try:
        fileObject = open(path, 'r')  # Get a list of filenames in given given file
        content = fileObject.read().splitlines()
    except:
        print("File Path Invalid!")
        exit(1)
    if (len(content) == 0):
        print("The file is empty!")  # If the text file is empty
        exit(0)
    categorize(content)


if __name__ == "__main__":
    argCount = len(sys.argv)
    if (argCount == 3):
        if (sys.argv[1] == "-f"):
            openFolder(sys.argv[2])  # Read filenames from folder

        elif (sys.argv[1] == "-t"):
            openText(sys.argv[2])  # Read filenames from text file

        elif (sys.argv[1] == "-i"):
            categorize([sys.argv[2]])
        else:
            invalid()

    elif (argCount == 1):
        currentDirectory = os.getcwd()  # Read filenames from current directory
        openFolder(currentDirectory)  # if no arguments are provided

    else:
        invalid()
