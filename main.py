# Name: Ruben Sanduleac
# Date: March 1, 2022
# Description: This program uses BeautifulSoup to scrape the billboard website for the
#              top 100 hit songs in the date specfied by the user. Once the program has all the information,
#              it will use the Spotify API to automatically generate the playlist with all the songs.


# TODO: capture a response from the user for the date that he would like to have a playlist from
# TODO: scrape the top 100 hits by looking at the songs titles'
import requests
from bs4 import BeautifulSoup
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

spotify_id = os.environ["SPOTIPY_CLIENT_ID"]
spotify_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
redirect_uri = os.environ["SPOTIPY_REDIRECT_URI"]

sp = spotipy.Spotify()

sp.auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                             redirect_uri=redirect_uri,
                             client_id=spotify_id,
                             client_secret=spotify_secret,
                             show_dialog=True,
                             cache_path="token.txt")

user_id = sp.current_user()["id"]

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
list_songs = []
for title in music_title:
    # TODO: Need to cleanup the specificity of the target scrape.
    song_title = title.get_text().strip()
    list_songs.append(song_title)
print(list_songs)