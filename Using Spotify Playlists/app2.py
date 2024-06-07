import json
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        # Return a default image if no results are found
        return "https://i.postimg.cc/0QNxYz4V/social.png"

st.header('Music Recommender System')

# Load music data from JSON file
with open('cb_recommendations.json', 'r') as file:
    cb_recommendations = json.load(file)

if st.button('Show All Songs'):
    col_count = min(len(cb_recommendations), 5)
    cols = st.columns(col_count)
    for i, song_data in enumerate(cb_recommendations):
        with cols[i % col_count]:  # cycle through columns
            track_name = song_data["Track Name"]
          
