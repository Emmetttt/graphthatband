from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests
import math

from .models import Band, Album, Reviews, BandSearch
from .forms import BandForm

def RetrieveInfo(name):
    i=0

    for checkDate in soupA.findAll('div', {"class" : "ratingRowContainer"}):
        if checkDate.contents == []:
            del albumYears[i]
            del albumNames[i]
            ##No i+1 since the length of the list has reduced by 1
        else:
            i = i+1
            
    for scores in soupA.findAll('div', {"class" : "rating"}):
        albumScores.append(int(scores.text))
        
    for j in albumYears:
        if j < 1900:
            del albumYears[j-1]
            del albumNames[j-1]
            del albumScores[j-1]

    k=0

    return albumNames, albumScores, albumYears, data, max_date, min_date, regression, max_score, min_score


def band_input(request):
    if request.method == "POST":
        Bform = BandForm(request.POST)
        if Bform.is_valid():
            try:
                bandname = Bform.cleaned_data.get('band_input')
                band = BandSearch(Bform.cleaned_data.get('band_input'))
                Bandform = BandForm()
                return render(request, 'music_grapher/graph.html', {'Bform': Bform,
                                                                    'regression': band.regression,
                                                                    'bandname': band.name,
                                                                    'data': band.data,
                                                                    'max_date': band.max_date,
                                                                    'min_date': band.min_date,
                                                                    'min_score': band.min_score,
                                                                    'max_score': band.max_score})
            except (NameError, AttributeError) as e:
                ErrorMessage = 'Band name "' + bandname + '" not found, please try again.'
                return render(request, 'music_grapher/index.html', {'Bform': Bform, 'Error': ErrorMessage})

    else:
        Bform = BandForm()
    return render(request, 'music_grapher/index.html', {'Bform': Bform, 'Error': ''})




def graph(request):
    return render(request, 'music_grapher/graph.html', {})
