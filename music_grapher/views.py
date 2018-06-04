from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import json

import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests
import math

from .models import Band, Album, Review, BandSearch
from .forms import BandForm

def index(request):
    return render(request, 'music_grapher/index.html', {'Error': ''})

def graph_band_search(request):
    ## Single band input
    bandname = request.GET.get('bandname')
    ErrorMessage = ''
    try:
        bandsearch = BandSearch(bandname)
        return render(request, 'music_grapher/graph.html', {'regression': bandsearch.band.regression,
                                                            'bandname': bandsearch.band.band_name,
                                                            'data': bandsearch.json_string,
                                                            'max_date': bandsearch.max_date,
                                                            'min_date': bandsearch.min_date,
                                                            'max_score': bandsearch.max_score,
                                                            'min_score': bandsearch.min_score})
    except (NameError, AttributeError, ObjectDoesNotExist) as e:
        ErrorMessage = 'The band "' + bandname + '" could not be found.'
        print(ErrorMessage, e)

    return render(request, 'music_grapher/index.html', {'Error': ErrorMessage})
