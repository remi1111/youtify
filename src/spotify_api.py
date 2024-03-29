""" Spotify API requests. """
import requests
import base64
import json
from secrets import *
import os

# Retrieve Spotify session token.
def get_token():
    # Retrieve ID and secret from .env
    clientId = os.getenv("SPOTIFY_CLIENT_ID")
    clientSecret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # Authorization
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    # Encode as Base64
    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']
    return token


def get_playlist(playlist_id, token, mylist=[], playlistUrl=None):
    if not playlistUrl:
        playlistUrl = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(url=playlistUrl, headers=headers)
    json_data = json.loads(res.content)

    a_list = analyze_playlist(json_data)
    newlist = mylist + a_list

    next_url = json_data['next']
    if not next_url:
        return newlist

    return get_playlist(playlist_id, token, newlist, next_url)

def analyze_playlist(json_data):
    mylist = []
    for song in json_data['items']:
        # album_artist = song['track']['album']['artists'][0]['name']
        # album_name = song['track']['album']['name']
        # release_date = song['track']['album']['release_date']
        song_artist = song['track']['artists'][0]['name']
        song_name = song['track']['name']
        song_dict = {'song artist': song_artist, 'song name': song_name}
        # song_dict = {'album artist': album_artist, 'album name': album_name, 'release date': release_date, 'song artist': song_artist, 'song name': song_name}
        mylist.append(song_dict)
    return mylist

def write_to_file(dict, filename):
    with open(filename, 'w') as file:
        file.write(json.dumps(dict))
