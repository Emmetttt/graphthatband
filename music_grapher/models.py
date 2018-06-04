import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
import json



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
    album_name = models.CharField(default="X", max_length=50)
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
        if self.__getRecord(name) != "NULL":
            bandnames = name.split(";")
            # if len(bandnames) == 1:
            #     self.band = Band.objects.get(band_name__iexact = self.__getRecord(name[0]))
            #     self.albums = list(Album.objects.filter(band_id = self.band.band_id))
            #     self.json_string = self.jsonify()
            #     self.MinMax() # Set min max values for dates and scores
            # else:
            self.json_string = {}
            self.all_band_names = ''
            for bandname in bandnames:
                self.band = Band.objects.get(band_name__iexact = self.__getRecord(bandname))
                self.all_band_names = self.all_band_names + self.band.band_name
                self.albums = list(Album.objects.filter(band_id = self.band.band_id))
                self.jsonify()
                self.MinMax()
            print(self.json_string)
        else:
            ValueError

    def __getRecord(self, name):
        ## Function to find the band from variations of the users input
        ## The-Beatles -> The Bealtes
        if Band.objects.filter(band_name__iexact = name.replace("-", " ")).count() == 1:
            return name.replace("-", " ")
        ## a ha -> a-ha
        if Band.objects.filter(band_name__iexact = name.replace(" ", "-")).count() == 1:
            return name.replace(" ", "-")
        ## ac dc -> ac/dc
        if Band.objects.filter(band_name__iexact = name.replace(" ", "/")).count() == 1:
            return name.replace(" ", "/")
        # check case
        if Band.objects.filter(band_name__iexact = name.lower()).count() == 1:
            return name.lower()
        if Band.objects.filter(band_name__iexact = name.title()).count() == 1:
            return name.title()
        if Band.objects.filter(band_name__iexact = name.upper()).count() == 1:
            return name.upper()
        else:
        ## Normal Input
            return name


    def jsonify(self):
<<<<<<< HEAD
        for album in self.albums:
            if self.band.band_name not in self.json_string:
                self.json_string[self.band.band_name] = [{
                    'band': self.band.band_name,
                    'name': album.album_name, 
                    'x': self.fract_year(str(album.date)),
                    'link': album.album_link,
                    'y': album.critic_score_avg,
                    'date': str(album.date)
                    }]
            else:
                self.json_string[self.band.band_name].append({
                    'band': self.band.band_name,
                    'name': album.album_name, 
                    'x': self.fract_year(str(album.date)),
                    'link': album.album_link,
                    'y': album.critic_score_avg,
                    'date': str(album.date)
                    })

    def AppendJson(self, dataToAppend):
        #print("\n\n\n\n" + dataToAppend + "\n\n\n\n")
        jsondata = json.dumps(dataToAppend)
        #print("\n\n\n\n" + dataToAppend + "\n\n\n\n")
        self.json_string['artistdata'].append(jsondata)
=======
        data = []
        k=0
        for album in self.albums: ##Gets data into javascript readable format
            data.append('{name: "' + album.album_name +
                        '",x: "' + self.fract_year(str(album.date)) + '",' +
                        'link: "' + album.album_link + '",' +
                        'y: ' + str(album.critic_score_avg) +
                        ',date: "' + str(album.date) + '"}')
            print(str(album.date))
            data[k] = data[k].replace("'", "")
            k = k+1

        data = str(data).replace("'", "")
        return data
>>>>>>> d9d98d1e9d9182979b4860f7774efa90d19b76cb

    def fract_year(self, date):
        #February 16,  2015 -> 2015.2something
        times = date.split("-")
        return str(int(times[0]) + (int(times[1])/13) + (int(times[2])/366))

    def MinMax(self):
        # Function to return min score, max score, min date, max date
        # Scores
        scores = [x.critic_score_avg for x in self.albums]
        self.max_score = max(scores)
        self.min_score = min(scores)

        # Dates
        dates = [x.date for x in self.albums]
        self.max_date = max(dates)
        self.max_date = int(self.max_date.year + 1)
        self.min_date = min(dates)
        self.min_date = int(self.min_date.year - 1)
        return



























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
                album.date = self.getdate(date)
            elif "Label" in row.text:
                label = row.text
                label = label[:-8]
                album.label = label
            elif "Genres" in row.text:
                genre = row.text
                genre = genre[:-9]
                album.genre = genre
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
        indiv = string.split(" ")
        if len(indiv) == 2:
            thisyear = indiv[1]
            thismonth = 1
            thisday = 1
        elif len(indiv) == 3:
            thisyear = indiv[2]
            thismonth = months[indiv[0]]
            thisday = 1
        else:
            thisyear = indiv[3]
            thismonth = months[indiv[0]]
            thisday = indiv[1]
            thisday = thisday.replace(",", "")
        #print(indiv, int(thisyear), int(thismonth), int(thisday))
        try:
            returndate = datetime.date(int(thisyear), int(thismonth), int(thisday))
        except ValueError:
            returndate = datetime.date(int(thisyear), int(thismonth), int(thisday)-2)
        return returndate

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
            if row.find("a", {"itemprop": "url", "rel": "nofollow"}):
                review["link"] = row.find("a", {"itemprop": "url", "rel": "nofollow"})['href']
            Review.objects.create(album_id = _album_id,
                                  score = review["score"],
                                  publication = review["publication"],
                                  review_link = review["link"])
