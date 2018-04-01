import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

#imports for BandSearch
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests
import math

class Band(models.Model):
    band_id = models.IntegerField(default=0) #Band PK
    band_name = models.CharField(max_length=50)
    regression = models.IntegerField(default=0)
    band_avg = models.IntegerField(default=50) #Default avg score
    band_divisiveness = models.IntegerField(default=0) #+/- on score

class Album(models.Model):
    album_id = models.IntegerField(default=0) #Album PK
    band_id = models.IntegerField(default=0) #Band FK
    album_name = models.CharField(max_length=50)
    score_avg = models.IntegerField(default=50) #Default to average score
    date = models.DateTimeField()
    review_summary = models.CharField(max_length=5000)

class Reviews(models.Model):
    album_id = models.IntegerField(default=0) #Album FK
    review = models.CharField(max_length=5000)
    score = models.IntegerField(default=50)
    key_words = models.CharField(max_length=1000) #list of words separated by ;
    band_comparisons = models.CharField(max_length=1000) #other bands mentions, ;

class BandSearch:
    def __init__(self, name):
        self.name = name.lower()
        self.nameDashed = name.replace(' ', '-')
        self.data = [] 
        self.max_date = 0 
        self.min_date = 0 
        self.regression = [] 
        self.max_score = [] 
        self.min_score = []
        self.albumData = []
        self.populateData()

    def __print__(self):
        print(self.name)
        print(self.data)
        print(self.max_date)
        print(self.min_date)
        print(self.max_score)
        print(self.min_score)
        print(self.albumData)

    def __soupSetup(self, website):
        ##Setup for any scraping
        page = website
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
        urllibpage = requests.get(page, headers=headers)
        soup = BeautifulSoup(urllibpage.text, "html.parser")
        return soup

    def getArtistPage(self):
        ##Pass through the band id and the AOTY url and it will populate self.bandInfo
        bandquery = Band.objects.get(band_name = self.nameDashed)
        url = 'https://www.albumoftheyear.org/artist/' + str(bandquery.band_id) + '/'
        artistsoup = self.__soupSetup(url)
        return artistsoup

    def getData(self, soup):
        albumContainer = soup.find('div', {"class" : "facetContent"})
        albumList = albumContainer.findChildren()
        for row in albumList: #for each album found
            #Is not a subheadline, needs to be split again
            album = {}
            datarow = row.findChildren()
            for data in datarow: #for each album find data
                if data.has_attr("class") and data.get("class")[0] == "date" and "album_year" not in album:
                    album["album_year"] = int(data.text)
                if data.has_attr("href") and "album_link" not in album:
                    album["album_link"] = "http://www.albumoftheyear.org" + data.get('href')
                if data.has_attr("class") and data.get("class")[0] == "albumTitle" and "album_title" not in album:
                    album["album_title"] = data.text
                #if data.has_attr("class") and data["class"][0] == "type" and "album_type" not in album:
                if data.has_attr("class") and data.get("class")[0] == "type" and "album_type" not in album:
                    album["album_type"] = data.text
                if data.has_attr("class") and data.get("class")[0] == 'ratingRowContainer':
                    ratingdiv = data.findChildren()
                    for rating in ratingdiv:
                        if "critic score" in rating.text and "\n" in rating.text and "critic_score" not in album:
                            album["critic_score"] = int(rating.find("div", {"class": "rating"}).text)
                            album["no_critic_reviews"] = rating.findAll("div", {"class": "ratingText"})[-1].text
                        if "user score" in rating.text and "\n" in rating.text and "user_score" not in album:
                            album["user_score"] = int(rating.find("div", {"class": "rating"}).text)
                            album["no_user_reviews"] = rating.findAll("div", {"class": "ratingText"})[-1].text
            if all([item in album for item in ["album_year", "album_link", "album_title"]]):
                self.albumData.append(album)

    def minMaxSet(self):
        if len(self.albumData) != 0:
            albumYears = [x["album_year"] for x in self.albumData]
            self.max_date = max(albumYears) + 2
            self.min_date = min(albumYears) - 2 

        if len(self.albumData) != 0:
            userScores = [x["user_score"] for x in self.albumData]
            criticScores = [x["critic_score"] for x in self.albumData]
            scores = userScores + criticScores
            if min(scores) < 5:
                self.min_score = min(scores)
            else:
                self.min_score = min(scores) - 5

            if max(scores) > 95:
                self.max_score = max(scores)
            else:
                self.max_score = max(scores) + 5



    def regression(self):
        if len(self.albumYears) == 0 or len(self.albumScores) == 0:
            return -1

        avgx = sum(self.albumYears)/len(self.albumYears)
        avgy = sum(self.albumScores)/len(self.albumScores)

        X = []
        Y = []
        sumxy = 0
        sumx2 = 0
        sumy2 = 0
        sumXminusmean = 0
        sumYminusmean = 0

        for j in range(self.albumYears - 1):
            X.append(self.albumYears[j] - avgx)
            Y.append(self.albumScores[j] - avgy)
            sumxy = sumxy + (Y[i]*X[i])
            sumx2 = sumx2 + X[i]**2
            sumy2 = sumy2 + Y[i]*Y[i]
            sumXminusmean = sumXminusmean + (self.albumYears[i] - avgx)**2
            sumYminusmean = sumYminusmean + (self.albumScores[i] - avgy)**2

        r = sumxy/math.sqrt(sumx2 * sumy2)
        stdevx = math.sqrt(sumXminusmean/(len(self.albumYears)-1))
        stdevy = math.sqrt(sumYminusmean/(len(self.albumScores)-1))

        b = r * (stdevx/stdevy)
        A = avgy - (b*avgx)

        lineX = [min(self.albumYears), max(self.albumYears)]
        lineY = [(lineX[0]*b)+A, (lineX[1]*b)+A]

        k=0
        regression = []
        for xy in lineX:
            regression.append([lineX[k],lineY[k]])
            k+=1

        self.regression = regression

    def jsonify(self):
        data = []
        k=0
        for value in self.albumData: ##Gets data into javascript readable format
            data.append('{name: "' + value["album_title"] + 
                        '",x: "' + str(value["album_year"]) + 
                        '",link: "' + value["album_link"] + 
                        '",y: ' + str(value["critic_score"]) + '}')
            data[k] = data[k].replace("'", "")
            k = k+1

        self.data = str(data).replace("'", "")

    def populateData(self):
        soup = self.getArtistPage()
        self.getData(soup)
        print(self.albumData)
        self.minMaxSet()
        #self.regression()
        self.jsonify()