import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np

SPOTIPY_CLIENT_ID='7f385d88c40b4829a2d8f715326cc2a2'
SPOTIPY_CLIENT_SECRET='35a728c9801d434fb7c89f061ffe2029'
SPOTIPY_REDIRECT_URI='http://localhost:8081'

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope,
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    open_browser=False
))

results = sp.current_user_saved_tracks()

# Create a new numpy array to store the tracks:
tracks = np.array([])

print('Starting to fetch data...')

# Iterate over all pages and put all the results in a csv:
while results:
    for idx, item in enumerate(results['items']):
        track = item['track']
        track_audio_features = sp.audio_features(track['id'])
        mapped_track = {
            'track_id': track['id'],
            'artists': ';'.join([artist['name'] for artist in track['artists']]),
            'album_name': track['album']['name'],
            'track_name': track['name'],
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'explicit': track['explicit'],
            'danceability': track_audio_features[0]['danceability'],
            'energy': track_audio_features[0]['energy'],
            'key': track_audio_features[0]['key'],
            'loudness': track_audio_features[0]['loudness'],
            'mode': track_audio_features[0]['mode'],
            'speechiness': track_audio_features[0]['speechiness'],
            'acousticness': track_audio_features[0]['acousticness'],
            'instrumentalness': track_audio_features[0]['instrumentalness'],
            'liveness': track_audio_features[0]['liveness'],
            'valence': track_audio_features[0]['valence'],
            'tempo': track_audio_features[0]['tempo'],
            'time_signature': track_audio_features[0]['time_signature'],
        }

        # Add the track to the array:
        tracks = np.append(tracks, mapped_track)

    if results['next']:
        results = sp.next(results)
    else:
        results = None

# Print the number of tracks:
print('Number of tracks:', len(tracks))

print(tracks)

# Create a dataframe with the tracks:
df = pd.DataFrame(tracks.tolist())

# Print the number of columns:
print('Number of columns:', len(df.columns))

# Get the dataset:
original_dataset = pd.read_csv('dataset.csv')

# Save the dataframe to a csv file:
df.to_csv('saved_dataset.csv', index=False)

# Find the diff in columns:
diff = np.setdiff1d(original_dataset.columns, df.columns)

# Print the diff:
print('Diff:', diff)