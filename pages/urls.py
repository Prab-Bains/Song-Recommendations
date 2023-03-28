# pages/urls.py
from django.urls import path
from .views import landing, homePageView, resultsPageView, homePost

urlpatterns = [
    path('', landing, name='landing'),
    path('/survey', homePageView, name='survey'),
    path('results/<str:genre>/<str:danceability>/<str:energy>/<str:acousticness>/<str:instrumentalness>/<str:valence>/', resultsPageView, name='results'),
    path('homePost/', homePost, name='homePost'),
]
