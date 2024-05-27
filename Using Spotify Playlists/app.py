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

def recommend(song):
    # Load song data from JSON file
    with open('cb_recommendations.json', 'r') as file:
        cb_recommendations = json.load(file)

    if song in cb_recommendations:
        recommended_music = cb_recommendations[song]
        return recommended_music
    else:
        return []

st.header('Music Recommender System')

# Load music data from JSON file
with open('cb_recommendations.json', 'r') as file:
    cb_recommendations = json.load(file)

music_list = list(cb_recommendations.keys())

selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music = recommend(selected_song)
    col_count = min(len(recommended_music), 5)
    cols = st.columns(col_count)
    for i, (recommended_song, artist) in enumerate(recommended_music):
        with cols[i]:
            st.text(recommended_song)
            st.image(get_song_album_cover_url(recommended_song, artist))

