import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Step 1: Get the data from Spotify (this is already in your code)
def get_playlist_data(playlist_id, access_token):
    sp = spotipy.Spotify(auth=access_token)
    playlist_tracks = sp.playlist_tracks(playlist_id, fields='items(track(id, name, artists, album(id, name)))')

    music_data = []
    for track_info in playlist_tracks['items']:
        track = track_info['track']
        track_name = track['name']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        album_name = track['album']['name']
        album_id = track['album']['id']
        track_id = track['id']

        audio_features = sp.audio_features(track_id)[0] if track_id != 'Not available' else None
        try:
            album_info = sp.album(album_id) if album_id != 'Not available' else None
            release_date = album_info['release_date'] if album_info else None
        except:
            release_date = None

        try:
            track_info = sp.track(track_id) if track_id != 'Not available' else None
            popularity = track_info['popularity'] if track_info else None
        except:
            popularity = None

        track_data = {
            'Track Name': track_name,
            'Artists': artists,
            'Album Name': album_name,
            'Album ID': album_id,
            'Track ID': track_id,
            'Popularity': popularity,
            'Release Date': release_date,
            'Duration (ms)': audio_features['duration_ms'] if audio_features else None,
            'Explicit': track_info.get('explicit', None),
            'External URLs': track_info.get('external_urls', {}).get('spotify', None),
            'Danceability': audio_features['danceability'] if audio_features else None,
            'Energy': audio_features['energy'] if audio_features else None,
            'Key': audio_features['key'] if audio_features else None,
            'Loudness': audio_features['loudness'] if audio_features else None,
            'Mode': audio_features['mode'] if audio_features else None,
            'Speechiness': audio_features['speechiness'] if audio_features else None,
            'Acousticness': audio_features['acousticness'] if audio_features else None,
            'Instrumentalness': audio_features['instrumentalness'] if audio_features else None,
            'Liveness': audio_features['liveness'] if audio_features else None,
            'Valence': audio_features['valence'] if audio_features else None,
            'Tempo': audio_features['tempo'] if audio_features else None,
        }

        music_data.append(track_data)

    df = pd.DataFrame(music_data)
    return df

playlist_id_list = [
    '64S8206Y2KJa2TzJCtPvf3', #Playlist 5 (Mix)
    '2XSpDIQ00elpbAifqSy8DC', #Playlist 2 (Metal)
    '3d2dL3wtLq8g3XiXKEn080', #Playlist 1 (Bangla)
    '71ALIJSdid4u92eDf4zhYQ', #Playlist 4 (HipHop)
    '5ABHKGoOzxkaa28ttQV9sE'  # Top 100 most streamed songs
]

music_df_list = [get_playlist_data(pid, access_token) for pid in playlist_id_list]
music_df = pd.concat(music_df_list, ignore_index=True, sort=False)

# Step 2: Preprocess the data
scaler = MinMaxScaler()
music_features = music_df[['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo']].values
music_features_scaled = scaler.fit_transform(music_features)

# Step 3: Prepare data for RNN
sequence_length = 5  # Define the sequence length for RNN
X, y = [], []
for i in range(len(music_features_scaled) - sequence_length):
    X.append(music_features_scaled[i:i + sequence_length])
    y.append(music_features_scaled[i + sequence_length])
X, y = np.array(X), np.array(y)

# Step 4: Build the RNN model
model = Sequential()
model.add(LSTM(64, input_shape=(sequence_length, X.shape[2]), return_sequences=True))
model.add(LSTM(64))
model.add(Dense(X.shape[2]))

model.compile(optimizer='adam', loss='mse')
model.summary()

# Step 5: Train the RNN model
model.fit(X, y, epochs=20, batch_size=32, validation_split=0.2)

# Step 6: Generate recommendations
def rnn_recommendations(input_song_name, num_recommendations=5):
    if input_song_name not in music_df['Track Name'].values:
        print(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return

    input_song_index = music_df[music_df['Track Name'] == input_song_name].index[0]
    input_sequence = music_features_scaled[input_song_index - sequence_length:input_song_index]

    if input_sequence.shape[0] != sequence_length:
        print(f"Not enough data to generate recommendations for '{input_song_name}'.")
        return

    input_sequence = np.expand_dims(input_sequence, axis=0)
    predicted_features = model.predict(input_sequence)

    similarity_scores = cosine_similarity(predicted_features, music_features_scaled)
    similar_song_indices = similarity_scores.argsort()[0][::-1][1:num_recommendations + 1]

    rnn_recommendations = music_df.iloc[similar_song_indices][['Track Name', 'Artists', 'Album Name', 'Release Date', 'Popularity']]
    return rnn_recommendations

# Example usage
input_song_name = "Breaking the Habit"
rnn_recommendations_list = rnn_recommendations(input_song_name, num_recommendations=10)
print(f"RNN recommended songs for '{input_song_name}':\n")
print(rnn_recommendations_list.to_string(index=False))
