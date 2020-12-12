# scrapper.py
import requests
from bs4 import BeautifulSoup
import sqlite3


def createBSObj(url):
    try:    #Get response from url
        response = requests.get(url)
    except:     #If it is not able to send request to website 
        print("Unable to connect to internet!")
        exit(1)

    if (response.status_code == 404):       #If website responded with 404 error
        print("Not able to get response from ", url)
  
    try:    #Convert it into Beautiful Soup object
        return BeautifulSoup(response.content, 'html.parser')
    except:
        print("Error in creating BS Object")
        exit(1)


def formatCategory(catName):    #Format category name for output
    catName = catName.capitalize()
    catName = catName.replace('-', ' ')
    return catName


if __name__ == "__main__":
    database = sqlite3.connect('extensions.db')
    cur = database.cursor()     #Connect to database

    domain = "https://www.file-extensions.org"
    BSObj = createBSObj(domain)     #Get scrapable BS object for URL

    subMenu = BSObj.find(id="submenu")      #Find submenu element 

    anchors = subMenu.find_all('a')     #Find all anchor tags in submenu
    if (not anchors):
        print("Anchor tags not found")
        exit(1)
    links = []

    for i in anchors:       #Make list of all links in submenu
        links.append(i['href']) 

    queryBase = "SELECT * FROM Extensions WHERE Name = '"
    links.pop(0)
    for i in links:
        url = domain + i        #URL to send request to all links in submenu
        i = i.split('/')
        category = i[len(i) - 1]        #Get category name from URL
        soupObj = createBSObj(url)      #Get scrapable BS object for URL
        table = soupObj.find(class_='extensiontable')
        rows = table.find_all('tr')     #list all rows in table
        rows.pop(0)
        print("Checking for new {0}...".format(formatCategory(category)))
        for row in rows:                #Check rows in table
            data = row.find_all('td')       
            extension = data[0].find('strong').text     #Get extension name
            description = data[1].text      #Get extension description
            query = queryBase + extension + "'"
            res = cur.execute(query)        #Check if information exists for the extenstion in database
            extInfo = res.fetchone()
            if (extInfo == None):       #If no information is present Insert it to database
                query = """INSERT INTO extensions(Name, Description, Category) VALUES("{0}", "{1}", "{2}")""".format(
                    extension, description, category)
                cur.execute(query)
                print("New extension: {0}\t{1}\t{2}".format(extension, description, category))      #Display newly inserted data
        database.commit()

    cur.close()         #Terminate connection to database
    database.close()
