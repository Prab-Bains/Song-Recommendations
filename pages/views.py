# pages/views.py
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
import pandas as pd
import pickle


def landing(request):
    return render(request, 'landing_page.html')


def homePageView(request):
    return render(request, 'home.html')


def homePost(request):
    genre = request.POST.get('genre')
    danceability = request.POST.get('danceability')
    energy = request.POST.get('energy')
    acousticness = request.POST.get('acousticness')
    instrumentalness = request.POST.get('instrumentalness')
    valence = request.POST.get('valence')

    # Here you can pass the values to the results page
    return redirect('results', genre=genre, danceability=danceability, energy=energy, acousticness=acousticness, instrumentalness=instrumentalness, valence=valence)


def resultsPageView(request, genre, danceability, energy, acousticness, instrumentalness, valence):
    data = pd.read_csv('SpotifyFeatures.csv')

    # Load the model from the pickle file and make predictions
    with open('spotify_model.pkl', 'rb') as file:
        model = pickle.load(file)

    user_input = {'genre': genre, 'danceability': danceability, 'energy': energy,
                  'acousticness': acousticness, 'instrumentalness': instrumentalness,
                  'valence': valence}

    # Convert user input to a numpy array
    user_input_array = pd.DataFrame(user_input, index=[0])[
        ['danceability', 'energy', 'acousticness', 'instrumentalness', 'valence']].to_numpy()

    # Reshape user input to match the expected shape of the model input
    user_input_array = user_input_array.reshape(1, -1)

    # Make predictions using the model
    prediction = model.predict_proba(user_input_array)[0]

    # Print the top 3 songs based on the predicted probability
    top_songs_indices = prediction.argsort()[::-1][:10]

    # Print the top 3 songs that match the user's preferred genre
    preferred_genre = user_input['genre']
    matches_genre = data[data['genre'] == preferred_genre].iloc[top_songs_indices][
        ['track_name', 'artist_name', 'genre']]

    context = {
        'genre': genre,
        'danceability': danceability,
        'energy': energy,
        'acousticness': acousticness,
        'instrumentalness': instrumentalness,
        'valence': valence,
        'matches_genre': matches_genre
    }

    return render(request, 'results.html', context)



