import json
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "536fcdb0f0ef43f0863f291ad78dc61c"
CLIENT_SECRET = "61ea0bb2b8ca46849c3fa368eda88ee3"

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

st.header('Music Information Display')

# Load music data from JSON file
with open('cb_recommendations.json', 'r') as file:
    cb_recommendations = json.load(file)

music_list = [track["Track Name"] for track in cb_recommendations]

selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show All Recommended Song Info'):
    st.write(f"Displaying information for all Recommended songs:")
    
    # Add CSS for styling the cards
    st.markdown("""
    <style>
    .card {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        transition: 0.3s;
        width: 100%;
        padding: 16px;
        text-align: center;
        margin-bottom: 16px;
        border-radius: 8px;
        background-color: #ffffff;
        color: #000000;
    }
    
    .card img {
        width: 100%;
        height: auto;
        border-radius: 8px;
    }
    
    .card h4, .card p {
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a grid layout with 3 columns
    cols = st.columns(3)
    for index, recommendation in enumerate(cb_recommendations):
        with cols[index % 3]:
            st.markdown(f"""
            <div class="card">
                <h4><b>{recommendation['Track Name']}</b></h4>
                <p>Artists: {recommendation['Artists']}</p>
                <p>Album Name: {recommendation['Album Name']}</p>
                <p>Release Date: {recommendation['Release Date']}</p>
                <p>Popularity: {recommendation['Popularity']}</p>
                <img src="{get_song_album_cover_url(recommendation['Track Name'], recommendation['Artists'])}" alt="Album Cover">
            </div>
            """, unsafe_allow_html=True)
