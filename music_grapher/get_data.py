import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests
import math

def RetrieveInfo(name):
    name = name.lower() ##lowers all the capitals
    nameDashed = name.replace(' ', '-') ##replace spaces with -
    firstLetter = name.replace('the ', '') ##removes "the " so it can find the first letter of the first name
    page = "http://www.albumoftheyear.org/artists/?id=" + firstLetter[0].upper() ##searches AOTY database for all beggining with first letter

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
    urllibpage = requests.get(page,headers=headers)
    soup = BeautifulSoup(urllibpage.text, "html.parser")
    Link = soup.find('a', href=re.compile('^/artist/[0-9]{1,7}-' + nameDashed)) ##Finds any link in the soup with can link to the beatles page
    Name = re.search('\/artist\/[0-9]{1,7}-(.*?)\/', str(Link)).group(0) ##extracts the links from <a> using regex group(0) prints the first match


    artistPage = 'http://www.albumoftheyear.org/' + Name ##load artist page directly
    urllibpageA = requests.get(artistPage, headers=headers)
    soupA = BeautifulSoup(urllibpageA.text, "html.parser")

    albumYears = []
    albumNames = []
    albumScores = []
    albumLinks = []
    art = []
    data = []

    for dates in soupA.findAll('div', {"class" : "date"}):
        albumYears.append(int(dates.text)) ##Change to integer from string so it can be graphed properly
    
    for titles in soupA.findAll('div', {"class" : "albumTitle"}):
        name = titles.text
        name = name.replace("'", "")
        albumNames.append(name)
        albumLink = "http://www.albumoftheyear.org" + titles.parent.get('href')
        albumLinks.append(albumLink)

    for albumArt in soupA.find_all('a'):
        if albumArt.img:
            print(albumArt.img['src'])
            art.append(albumArt)

RetrieveInfo("Leonard Cohen")