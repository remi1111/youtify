""" Spotify API requests. """
import base64
import json
# from secrets import *
import os
import sys

import requests

def get_token():
    """ Retrieve spotify api token """
    # Retrieve ID and secret from .env
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # Authorization
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    # Encode as Base64
    message = f"{client_id}:{client_secret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    headers['Authorization'] = f"Basic {base64_message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data, timeout=10)
    if r is None:
        print("Spotify request timed out", file=sys.stderr)
        sys.exit(101)

    token = r.json()['access_token']
    return token


def get_playlist(playlist_id, token, mylist, playlist_url=None):
    """ Retrieve playlist form spotify """
    if not playlist_url:
        playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(url=playlist_url, headers=headers, timeout=10)
    if res is None:
        print("Spotify request timed out", file=sys.stderr)
        sys.exit(101)

    json_data = json.loads(res.content)

    a_list = analyze_playlist(json_data)
    newlist = mylist + a_list

    next_url = json_data['next']
    if not next_url:
        return newlist

    return get_playlist(playlist_id, token, newlist, next_url)

def analyze_playlist(json_data):
    """ Stores data for each song in a dictionary. """
    mylist = []
    for song in json_data['items']:
        album_artist = song['track']['album']['artists'][0]['name']
        album_name = song['track']['album']['name']
        release_date = song['track']['album']['release_date']
        song_artist = song['track']['artists'][0]['name']
        song_name = song['track']['name']
        song_dict = {'album artist': album_artist,
                     'album name': album_name,
                     'release date': release_date,
                     'song artist': song_artist,
                     'song name': song_name}
        mylist.append(song_dict)
    return mylist

def write_to_file(song_dict, filename):
    """ Write a playlist dictionary to a file. """
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(json.dumps(song_dict))
