from music_grapher.models import Band, Album, Reviews, BandSearch

import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests
import math

def openPage(page):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
    urllibpage = requests.get(page, headers=headers)
    soup = BeautifulSoup(urllibpage.text, "html.parser")

def getLastBand():
    x = Band.objects.latest('band_id')
    return x.band_id+1

def getBandData(soup, band_fk):
    albumContainer = soup.find('div', {"class" : "facetContent"})
    albumList = albumContainer.findChildren()
    for row in albumList: #for each album found
        #Is not a subheadline, needs to be split again
        album = {
            "album_year": 0,
            "album_link": "X",
            "album_title": "X",
            "album_type": "X",
            "critic_score": 0,
            "user_score": 0,
        }

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
        #If data is complete, insert to DB
        if all([item in album for item in ["album_year", "album_link", "album_title"]]):
            if album["critic_score"] + album["user_score"] != 0:
                if Album.objects.filter(album_link = album['album_link']).count() == 0:
                    #Enter data
                    Album.objects.create(band_id=band_fk,
                                         album_name = album['album_title'],
                                         album_link = album['album_link'],
                                         critic_score_avg = album['critic_score'],
                                         user_score_avg = album['user_score'],
                                         date = album['album_year'])

if __name__ == "__main__":
    i = getLast()
    while i < 3000:#40000:
        url = 'https://www.albumoftheyear.org/artist/' + str(id) + '/'
        band_soup = openPage(url)
        getBandData(band_soup, i)

