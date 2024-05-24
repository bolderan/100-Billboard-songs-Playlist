clientID ="Your Client ID"
clientsecret = "Client Secret"
redirect_URL = "http://Demopotify.com" # your orignal URL 

OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

URL = "https://www.billboard.com/charts/hot-100/"
date = input("Which year do you wnat to travel to? Type date in formate (YYYY-MM-DD): ")
response = requests.get(f"{URL}{date}/")
soup = BeautifulSoup(response.text,"html.parser")
song_name_span = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_name_span]
print(song_names)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=redirect_URL,
        client_id=clientID,
        client_secret=clientsecret,
        show_dialog=True,
        cache_path="token.txt", # You will need to save your access token in different file name "token.txt"
        username="Yourusername", #Your username 
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
