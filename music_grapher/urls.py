from django.conf.urls import *

from . import views

app_name = 'music_grapher'
urlpatterns = [
    url('', views.band_input, name='index'),
    url('graph/', views.graph, name='graph'),
]

