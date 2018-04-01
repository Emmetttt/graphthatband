import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests

def RetrieveInfo(name):
    page = "http://www.metacritic.com/person/" + name
    
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
    urllibpage = requests.get(page,headers=headers)
    soup = BeautifulSoup(urllibpage.text, "lxml")
    mydivs = soup.findAll("table", { "class" : "credits person_credits" })
    mytrs = soup.findAll("tr")
    #print(mytrs)

    albumNames = []
    albumScores = []
    albumYears = []

    for score in soup.findAll("span", { "class" : "metascore_w small release positive"}):
        albumScores.append(score.string)

    for year in soup.findAll("td", { "class" : "year" }):
        alyear = year.string
        albumYears.append(alyear.strip())

    for name in soup.findAll("a", href=re.compile('^/music/')):
        albumNames.append(name.string)

    all_together = list(zip(albumNames[2:], albumScores, albumYears))
    return all_together

def printtt(name):
    return print(name)
