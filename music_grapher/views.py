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
        print(bandsearch.json_string)
        return render(request, 'music_grapher/graph.html', {'regression': bandsearch.band.regression,
                                                            'bandname': bandsearch.band.band_name,
                                                            'data': bandsearch.json_string,
                                                            'max_date': bandsearch.max_date,
                                                            'min_date': bandsearch.min_date,
                                                            'max_score': bandsearch.max_score,
                                                            'min_score': bandsearch.min_score})
    except (NameError, AttributeError, ObjectDoesNotExist) as e:
        ErrorMessage = 'Band name "'# + bandname + '" not found, please try again.'

    return render(request, 'music_grapher/index.html', {'Error': ''})

# def band_input(request, urlbandname='none'):
#     ## Single band input
#     if (request.method == "POST" and 'singleBandPost' in request.POST):
#         Bform = BandForm(request.POST)
#         if Bform.is_valid():
#             try:
#                 bandname = Bform.cleaned_data.get('band_input')
#                 bandsearch = BandSearch(bandname)
#                 return render(request, 'music_grapher/graph.html', {'Bform': Bform,
#                                                                     'regression': bandsearch.band.regression,
#                                                                     'bandname': bandsearch.band.band_name,
#                                                                     'data': bandsearch.json_string,
#                                                                     'max_date': bandsearch.max_date,
#                                                                     'min_date': bandsearch.min_date,
#                                                                     'max_score': bandsearch.max_score,
#                                                                     'min_score': bandsearch.min_score})
#             except (NameError, AttributeError, ObjectDoesNotExist) as e:
#                 ErrorMessage = 'Band name "' + bandname + '" not found, please try again.'
#                 return render(request, 'music_grapher/index.html', {'Bform': Bform, 'Error': ErrorMessage})

#     ## Multiple band input
#     ## Will be passed through the url via /bandname=bright-eyes+bon-iver+m-ward
#     elif request.method == "POST" and 'addBandPost' in request.POST:
#         Bform = BandForm(request.POST)
#         if Bform.is_valid():
#             try:
#                 bandname = Bform.cleaned_data.get('band_input')
#                 bandsearch = BandSearch(bandname)
#                 previous_json = json.dumps(Bform.data.get('json_string'))
#                 print("\n\n\n" + previous_json)
#                 print("\n\n\n" + bandsearch.json_string)
#                 bandsearch.json_string = bandsearch.json_string['artistdata'].append(previous_json)
#                 print("\n\n\n" + bandsearch.json_string)
#                 #bandsearch.AppendJson(Bform.data.get('json_string'))
#                 #print(bandsearch.json_string)
#                 return render(request, 'music_grapher/graph.html', {'Bform': Bform,
#                                                                     'regression': bandsearch.band.regression,
#                                                                     'bandname': bandsearch.band.band_name,
#                                                                     'data': bandsearch.json_string,
#                                                                     'max_date': bandsearch.max_date,
#                                                                     'min_date': bandsearch.min_date,
#                                                                     'max_score': bandsearch.max_score,
#                                                                     'min_score': bandsearch.min_score})
#             except (NameError, AttributeError, ObjectDoesNotExist) as e:
#                 ErrorMessage = 'Band name "' + bandname + '" not found, please try again.\n' + str(e)
#                 return render(request, 'music_grapher/index.html', {'Bform': Bform, 'Error': ErrorMessage})

#     else:
#         Bform = BandForm()
#     return render(request, 'music_grapher/index.html', {'Bform': Bform, 'Error': ''})