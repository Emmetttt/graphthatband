from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import urllib.request
from bs4 import BeautifulSoup
import re
import time
import requests
import math

from .models import Band, Album, Review, BandSearch
from .forms import BandForm

def band_input(request):
    if request.method == "POST":
        Bform = BandForm(request.POST)
        if Bform.is_valid():
            try:
                bandname = Bform.cleaned_data.get('band_input')
                bandsearch = BandSearch(Bform.cleaned_data.get('band_input'))
                Bandform = BandForm()
                return render(request, 'music_grapher/graph.html', {'Bform': Bform,
                                                                    'regression': bandsearch.band.regression,
                                                                    'bandname': bandsearch.band.band_name,
                                                                    'data': bandsearch.json_string,
                                                                    'max_date': bandsearch.max_date,
                                                                    'min_date': bandsearch.min_date,
                                                                    'max_score': bandsearch.max_score,
                                                                    'min_score': bandsearch.min_score})
            except (NameError, AttributeError, ObjectDoesNotExist) as e:
                ErrorMessage = 'Band name "' + bandname + '" not found, please try again.'
                return render(request, 'music_grapher/index.html', {'Bform': Bform, 'Error': ErrorMessage})

    else:
        Bform = BandForm()
    return render(request, 'music_grapher/index.html', {'Bform': Bform, 'Error': ''})




def graph(request):
    return render(request, 'music_grapher/graph.html', {})
