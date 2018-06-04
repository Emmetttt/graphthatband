from django.urls import path

from . import views

app_name = 'music_grapher'
urlpatterns = [
    path('', views.index, name='index'),
    path('band/', views.graph_band_search),
]

