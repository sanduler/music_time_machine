# Name: Ruben Sanduleac
# Date: March 1, 2022
# Description: This program uses BeautifulSoup to scrape the billboard website for the
#              top 100 hit songs in the date specfied by the user. Once the program has all the information,
#              it will use the Spotify API to automatically generate the playlist with all the songs.


import requests
from bs4 import BeautifulSoup
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

# environmental variables used in the program
spotify_id = os.environ["SPOTIPY_CLIENT_ID"]
spotify_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
redirect_uri = os.environ["SPOTIPY_REDIRECT_URI"]

# create an object for the Spotify authentication
spotify_app = spotipy.Spotify()

# pass the required methods to Spotify Authentication API
spotify_app.auth_manager = SpotifyOAuth(scope="playlist-modify-private",
                                        redirect_uri=redirect_uri,
                                        client_id=spotify_id,
                                        client_secret=spotify_secret,
                                        show_dialog=True,
                                        cache_path="token.txt")
# get the user if
user_id = spotify_app.current_user()["id"]
# capture the input for the year that the program will search for to scrape.
year = input("Which year do you want to travel to? Type the data in this format: YYYY-MM-DD: ")
# pass the year to the billboard website which will be used to scrape the data
URL = f"https://www.billboard.com/charts/hot-100/{year}"
# get a response from the webpage
response = requests.get(URL)
# convert the response to text
top_hits = response.text
# print(top_hits)
# create a new BeautifulSoup object for this website and parse the text
soup = BeautifulSoup(top_hits, "html.parser")
# create a list of all the top movies including the ranking
music_title = soup.find_all(name="h3",
                            class_="c-title a-no-trucate a-font-primary-bold-s u-"
                                   "letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 "
                                   "u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis "
                                   "u-max-width-330 u-max-width-230@tablet-only",
                            id="title-of-a-story")
# generate a list of songs
song_uris = []
# loop through each title of the songs
for title in music_title:
    # remove the white space and \n in the lust
    song_title = title.get_text().strip()
    result = spotify_app.search(q=f"track:{song_title}", type="track")
    # print(result)
    # try to get the songs URI and append the song URI to the list
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    # in the case of an index error then let the user know that the songs is not in the spotify library
    except IndexError:
        print(f"{song_title} doesn't exist in Spotify. Skipped.")
# create a new playlist by pasing the user if the year that the user requested as well as set it to be
# non-collaborative and private.
playlist = spotify_app.user_playlist_create(user=user_id, name=f"{year} Billboard 100", collaborative=False,
                                            public=False)
# add the list of songs to the playlist.
spotify_app.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
