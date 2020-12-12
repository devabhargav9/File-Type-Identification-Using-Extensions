# scrapper.py
import requests
from bs4 import BeautifulSoup
import sqlite3


def createBSObj(url):
    response = requests.get(url)        #Get response from url
    if (response.status_code == 404):        #If website responded with 404 error
        print("Not able to get response from ", url)

    try:        #Convert it into Beautiful Soup object
        return BeautifulSoup(response.content, 'html.parser')
    except:
        print("Error in creating BS Object")
        exit(1)


if __name__ == "__main__":
    database = sqlite3.connect('extensions.db')
    cur = database.cursor()         #Connect to database

    domain = "https://www.file-extensions.org"
    BSObj = createBSObj(domain)         #Get scrapable BS object for URL

    subMenu = BSObj.find(id="submenu")        #Find submenu element 

    anchors = subMenu.find_all('a')           #Find all anchor tags in submenu
    if (not anchors):
        print("Anchor tags not found")
        exit(1)
    links = []

    for i in anchors:                #Make list of all links in submenu
        links.append(i['href'])
    links.pop(0)
    # print(links)

    queryBase = "INSERT INTO extensions(Name, Description, Category) VALUES"

    for i in links:
        url = domain + i            #URL to send request to all links in submenu
        i = i.split('/')
        category = i[len(i) - 1]        #Get category name from URL
        print("URL: ", url)
        soupObj = createBSObj(url)          #Get scrapable BS object for URL
        table = soupObj.find(class_='extensiontable')
        rows = table.find_all('tr')         #list all rows in table
        rows.pop(0)
        for row in rows:
            data = row.find_all('td')
            extension = data[0].find('strong').text         #Get extension name
            description = data[1].text          #Get extension description
            value = "('" + extension + "', '" + description + "', '" + category + "')"
            query = queryBase + value           #Query for inserting into data base

            try:
                cur.execute(query)          #Insert into database
            except Exception as e:
                print(e, end=" ")
                print("While inserting values:", value)
        database.commit()

    cur.close()         #Terminate connection to database
    database.close()        
