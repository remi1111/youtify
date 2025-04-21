""" Spotify API requests. """
import base64
import json
import os
import sys

import requests


class SongData:
    """ SongData class stores important song data. """
    album_artist = None
    album_name = None
    release_date = None
    release_year = None
    song_artist = None
    song_name = None
    track_num = None
    disc_num = None
    track_total = None
    disc_total = None

    def __init__(self, song_dict):
        self.album_artist = song_dict['track']['album']['artists'][0]['name']
        self.album_name = song_dict['track']['album']['name']
        self.release_date = song_dict['track']['album']['release_date']
        self.song_artist = song_dict['track']['artists'][0]['name']
        self.song_name = song_dict['track']['name']
        self.track_num = song_dict['track']['track_number']
        self.disc_num = song_dict['track']['disc_number']
        self.track_total = song_dict['track']['album']['total_tracks']
        self.disc_total = 1

        if self.release_date:
            self.release_year = self.release_date[:4]

    def __str__(self):
        return f"{self.song_artist} - {self.song_name}\n" \
                f"Release Date: {self.release_date}\n" \
                f"Album: {self.album_artist} - {self.album_name}\n" \
                f"Track: {self.track_num}/{self.track_total}\n" \
                f"Disc: {self.disc_num}/{self.disc_total}"

class PlaylistData:
    """ Class that retrieves songs from spotify and puts them in song_list. """
    song_list: list[SongData] = []
    playlist_id = None
    playlist_base_url = "https://api.spotify.com/v1/playlists/{}/tracks"

    def __init__(self):
        self._auth = SpotifyAuth()

    def get_playlist_data(self, playlist_id, playlist_url=None):
        """ Retrieve playlist form spotify """
        if not playlist_url:
            playlist_url = "https://api.spotify.com/v1/playlists/{}/tracks"

        res = requests.get(url=playlist_url, headers=self._auth._headers, timeout=10)
        if res is None:
            print("Spotify request timed out", file=sys.stderr)
            sys.exit(101)

        json_data = json.loads(res.content)
        self.analyze_playlist_data(json_data)

        next_url = json_data['next']
        if next_url:
            self.get_playlist_data(playlist_id, next_url)

    def analyze_playlist_data(self, json_data):
        """ Stores data for each song in a SongData object. """
        for song in json_data['items']:
            song_data = SongData(song)
            self.song_list.append(song_data)

    def __str__(self):
        return self.song_list


class SpotifyAuth:
    """ Class for authentication on spotify. """
    _api_token = None

    def __init__(self):
        self.get_token()
        self._headers = {
            "Authorization": "Bearer " + self._api_token
        }

    def get_token(self):
        """ Retrieve spotify api token. """
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

        self._api_token = r.json()['access_token']
