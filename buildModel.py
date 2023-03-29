import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

# Load the dataset
data = pd.read_csv('/Users/prabhjeetbains/Desktop/BCIT/Data sets/SpotifyFeatures.csv')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Define the features and target variable
X = data[['danceability', 'energy', 'acousticness', 'instrumentalness', 'valence']]
y = data['popularity']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the logistic regression model
model = LogisticRegression()

# Train the model using the training data
model.fit(X_train, y_train)

# Save the model to a pickle file
with open('spotify_model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Load the model from the pickle file and make predictions
with open('spotify_model.pkl', 'rb') as file:
    model = pickle.load(file)

user_input = {'genre': 'Rap', 'danceability': 4, 'energy': 4, 'acousticness': 2, 'instrumentalness': 2, 'valence': 3}

# Convert user input to a numpy array
user_input_array = pd.DataFrame(user_input, index=[0])[['danceability', 'energy', 'acousticness', 'instrumentalness', 'valence']].to_numpy()

# Reshape user input to match the expected shape of the model input
user_input_array = user_input_array.reshape(1, -1)

# Make predictions using the model
prediction = model.predict_proba(user_input_array)[0]

# Print the top 3 songs based on the predicted probability
top_songs_indices = prediction.argsort()[::-1][:10]

# Print the top 3 songs that match the user's preferred genre
preferred_genre = user_input['genre']
matches_genre = data[data['genre'] == preferred_genre].iloc[top_songs_indices][['track_name', 'artist_name', 'genre']]
print(f'Top songs that match the genre "{preferred_genre}":')
print(matches_genre)
print(type(matches_genre))
