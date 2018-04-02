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
import datetime

class Band(models.Model):
    band_id = models.IntegerField(default=0) #Band PK
    band_name = models.CharField(max_length=50)
    regression = models.IntegerField(default=0)
    band_avg = models.IntegerField(default=50) #Default avg score
    band_divisiveness = models.IntegerField(default=0) #+/- on score

class Album(models.Model):
    band_id = models.IntegerField(default=0) #Band FK
    album_name = models.CharField(default="x", max_length=50)
    album_link = models.CharField(default="x", max_length=200)
    critic_score_avg = models.IntegerField(default=-1) #Default to average score
    number_critic_reviews = models.IntegerField(default=0)
    user_score_avg = models.IntegerField(default=-1) #Default to average score
    number_user_reviews = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)
    label = models.CharField(default="x", max_length=50)
    genre = models.CharField(default="x", max_length=50)
    review_summary = models.CharField(default="x", max_length=5000)

class Review(models.Model):
    album_id = models.IntegerField(default=0) #Album FK
    review = models.CharField(max_length=5000)
    publication = models.CharField(max_length=50)
    score = models.IntegerField(default=50)
    review_link = models.CharField(max_length=100)
    key_words = models.CharField(max_length=1000) #list of words separated by ;
    band_comparisons = models.CharField(max_length=1000) #other bands mentions, ;

class BandSearch:
    def __init__(self, name):
        self.band = Band.objects.get(band_name = name)
        self.albums = list(Album.objects.filter(band_id = self.band.band_id))
        self.json_string = self.jsonify()
        self.min_date = 1900
        self.max_date = 2020
        self.min_score = 0
        self.max_score = 100

    def jsonify(self):
        data = []
        k=0
        for album in self.albums: ##Gets data into javascript readable format
            data.append('{name: "' + album.album_name + 
                        '",x: "' + self.fract_year(str(album.date)) + 
                        '",link: "' + album.album_link + 
                        '",y: ' + str(album.critic_score_avg) + '}')
            data[k] = data[k].replace("'", "")
            k = k+1

        data = str(data).replace("'", "")
        return data

    def fract_year(self, date):
        #February 16,  2015 -> 2015.2something
        times = date.split("-")
        return str(int(times[0]) + (int(times[1])/13) + (int(times[2])/366))

    def MinMax(self):
        pass




















class PopDB:
    def __init__(self):
        print("PopDB Start")
        i = self.getLastBand()
        print("ID: ", i)
        while i < 3000:#40000:
            url = 'https://www.albumoftheyear.org/artist/' + str(i) + '/'
            band_soup = self.openPage(url)
            self.getBandData(band_soup, i)
            #Basic data retreived from band page, now get specific album data
            hrefs = [a.album_link for a in list(Album.objects.filter(band_id=i))]
            album_id = [int(a.id) for a in list(Album.objects.filter(band_id=i))]
            count = 0
            for album_href in hrefs:
                album_soup = self.openPage(album_href)
                self.getAlbumData(album_soup, album_id[count])
                self.getReviewData(album_soup, album_id[count])
                count+=1

            print("ID: ", i)
            i+=1

    def openPage(self, page):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
        urllibpage = requests.get(page, headers=headers)
        soup = BeautifulSoup(urllibpage.text, "html.parser")
        return soup

    def getLastBand(self):
        x = Band.objects.latest('band_id')
        return x.band_id+1

    def getBandData(self, soup, band_fk):
        bandName = soup.find('h1', {"class": "artistHeadline"}).text
        albumContainer = soup.find('div', {"class" : "facetContent"})
        albumList = albumContainer.findChildren()
        for row in albumList: #for each album found
            #Is not a subheadline, needs to be split again
            album = {
                "band_name": bandName,
                "album_link": "X",
                "album_title": "X",
                "album_type": "X",
                "critic_score": 0,
                "no_critic_reviews": 0,
                "user_score": 0,
                "no_user_reviews": 0,
            }

            datarow = row.findChildren()
            for data in datarow: #for each album find data
                if data.has_attr("href"):
                    album["album_link"] = "http://www.albumoftheyear.org" + data.get('href')
                if data.has_attr("class") and data.get("class")[0] == "albumTitle":
                    album["album_title"] = data.text
                #if data.has_attr("class") and data["class"][0] == "type" and "album_type" not in album:
                if data.has_attr("class") and data.get("class")[0] == "type":
                    album["album_type"] = data.text
                if data.has_attr("class") and data.get("class")[0] == 'ratingRowContainer':
                    ratingdiv = data.findChildren()
                    for rating in ratingdiv:
                        if "critic score" in rating.text and "\n" in rating.text:
                            album["critic_score"] = int(rating.find("div", {"class": "rating"}).text)
                            album["no_critic_reviews"] = int(rating.findAll("div", {"class": "ratingText"})[-1].text[1:-1])
                        if "user score" in rating.text and "\n" in rating.text:
                            album["user_score"] = int(rating.find("div", {"class": "rating"}).text)
<<<<<<< HEAD
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


















class PopDB:
    def __init__(self):
        print("PopDB Start")
        i = self.getLastBand()
        print("ID: ", i)
        while i < 3000:#40000:
            url = 'https://www.albumoftheyear.org/artist/' + str(i) + '/'
            band_soup = self.openPage(url)
            self.getBandData(band_soup, i)
            #Basic data retreived from band page, now get specific album data
            hrefs = [a.album_link for a in list(Album.objects.filter(band_id=i))]
            album_id = [int(a.id) for a in list(Album.objects.filter(band_id=i))]
            count = 0
            for album_href in hrefs:
                album_soup = self.openPage(album_href)
                self.getAlbumData(album_soup, album_id[count])
                self.getReviewData(album_soup, album_id[count])
                count+=1

            print("ID: ", i)
            i+=1

    def openPage(self, page):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
        urllibpage = requests.get(page, headers=headers)
        soup = BeautifulSoup(urllibpage.text, "html.parser")
        return soup

    def getLastBand(self):
        x = Band.objects.latest('band_id')
        return x.band_id+1

    def getBandData(self, soup, band_fk):
        bandName = soup.find('h1', {"class": "artistHeadline"}).text
        albumContainer = soup.find('div', {"class" : "facetContent"})
        albumList = albumContainer.findChildren()
        for row in albumList: #for each album found
            #Is not a subheadline, needs to be split again
            album = {
                "band_name": bandName,
                "album_link": "X",
                "album_title": "X",
                "album_type": "X",
                "critic_score": 0,
                "no_critic_reviews": 0,
                "user_score": 0,
                "no_user_reviews": 0,
            }

            datarow = row.findChildren()
            for data in datarow: #for each album find data
                if data.has_attr("href"):
                    album["album_link"] = "http://www.albumoftheyear.org" + data.get('href')
                if data.has_attr("class") and data.get("class")[0] == "albumTitle":
                    album["album_title"] = data.text
                #if data.has_attr("class") and data["class"][0] == "type" and "album_type" not in album:
                if data.has_attr("class") and data.get("class")[0] == "type":
                    album["album_type"] = data.text
                if data.has_attr("class") and data.get("class")[0] == 'ratingRowContainer':
                    ratingdiv = data.findChildren()
                    for rating in ratingdiv:
                        if "critic score" in rating.text and "\n" in rating.text:
                            album["critic_score"] = int(rating.find("div", {"class": "rating"}).text)
                            album["no_critic_reviews"] = int(rating.findAll("div", {"class": "ratingText"})[-1].text[1:-1])
                        if "user score" in rating.text and "\n" in rating.text:
                            album["user_score"] = int(rating.find("div", {"class": "rating"}).text)
=======
>>>>>>> b2d4da7d36c530951c0017e0a080b8fb36f75d16
                            album["no_user_reviews"] = int(rating.findAll("div", {"class": "ratingText"})[-1].text[1:-1])
            #If data is complete, insert to DB
            if album["critic_score"] + album["user_score"] != 0:
                    #Check if the band already exists in DB
                    if Band.objects.filter(band_name = album['band_name']).count() == 0:
                        Band.objects.create(band_id = band_fk,
                                            band_name = album['band_name'])
                    #Check if the album is already in the DB
                    if Album.objects.filter(album_link = album['album_link']).count() == 0:
                        #Enter data
                        Album.objects.create(band_id=band_fk,
                                             album_name = album['album_title'],
                                             album_link = album['album_link'],
                                             critic_score_avg = album['critic_score'],
                                             number_critic_reviews = album["no_critic_reviews"],
                                             number_user_reviews = album["no_user_reviews"],
                                             user_score_avg = album['user_score'])

    def getAlbumData(self, soup, album_id):
        album = Album.objects.get(id=album_id)
        info = soup.find("div", {"class": "albumTopBox info"})
        for row in info.findAll("div", {"class": "detailRow"}):
            if "Release Date" in row.text:
                date = row.text
                date = date[:-15]
<<<<<<< HEAD
                album.date = date
=======
                album.date = self.getdate(date)
                print(album.date)
>>>>>>> b2d4da7d36c530951c0017e0a080b8fb36f75d16
            elif "Label" in row.text:
                label = row.text
                label = label[:-8]
                album.label = label
            elif "Genres" in row.text:
                genre = row.text
                genre = genre[:-9]
                album.genre = genre
<<<<<<< HEAD
=======
        #save changes
        album.save()

    def getdate(self, string):
        #February 16,  2015 -> 2015-02-16
        months = {
            "January": "01",
            "February": "02",
            "March": "03",
            "April": "04",
            "May": "05",
            "June": "06",
            "July": "07",
            "August": "08",
            "September": "09",
            "October": "10",
            "December": "11",
            "November": "12",
        }
        print(string)
        indiv = string.split(" ")
        if len(indiv) < 3:
            thisyear = string.relace(" ")
            thismonth = 0
            thisday = 0
        else:
            thisyear = indiv[3]
            thismonth = months[indiv[0]]
            thisday = indiv[1]
            thisday = thisday.replace(",", "")
            if int(thisday) < 10:
                thisday = "0" + thisday
        return datetime.date(int(thisyear), int(thismonth), int(thisday))
>>>>>>> b2d4da7d36c530951c0017e0a080b8fb36f75d16

    def getReviewData(self, soup, _album_id):
        reviews = soup.find("div", {"id": "critics", "class": "section"})
        for row in reviews.findAll("div", {"itemprop": "review"}):
            review = {
                "score": "",
                "publication": "",
                "link": ""
                }
            review["score"] = row.find("span", {"itemprop": "ratingValue"}).text
            review["publication"] = row.find("span", {"itemprop": "name"}).text
            review["link"] = row.find("a", {"itemprop": "url", "rel": "nofollow"})['href']
            Review.objects.create(album_id = _album_id,
                                  score = review["score"],
                                  publication = review["publication"],
                                  review_link = review["link"])