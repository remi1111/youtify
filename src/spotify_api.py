""" Spotify API requests. """
import base64
import json
import os
import sys

from dotenv import load_dotenv
import requests


class SongData:
    """ SongData class stores important song data. """
    album_artist: str = None
    album_name: str = None
    release_date: str = None
    release_year: int = None
    song_artist: str = None
    song_name: str = None
    track_num: int = None
    disc_num: int = None
    track_total: int = None
    disc_total: int = None

    def __init__(self, song_dict: str) -> None:
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
            self.release_year = int(self.release_date[:4])

    def get_data_as_dict(self) -> dict:
        return {'album artist': self.album_artist,
                'album name': self.album_name,
                'release date': self.release_date,
                'release year': self.release_year,
                'song artist': self.song_artist,
                'song name': self.song_name,
                'track num': self.track_num,
                'track total': self.track_total,
                'disc num': self.disc_num,
                'disc total': self.disc_total}

    def get_data_as_csv(self) -> str:
        return f"\"{self.song_artist}\";\"{self.song_name}\";\"{self.album_artist}\";\"{self.album_name}\";\"{self.release_date}\";\"{self.track_num}\";\"{self.track_total}\";\"{self.disc_num}\";\"{self.disc_total}\""

    def __str__(self) -> str:
        return f"{self.song_artist} - {self.song_name}\n" \
                f"Release Date: {self.release_date}\n" \
                f"Album: {self.album_artist} - {self.album_name}\n" \
                f"Track: {self.track_num}/{self.track_total}\n" \
                f"Disc: {self.disc_num}/{self.disc_total}"


class PlaylistData:
    """ Class that retrieves songs from spotify and puts them in song_list. """
    song_list: list[SongData] = []
    playlist_id: str = None

    def __init__(self, playlist_id: str) -> None:
        self._auth = SpotifyAuth()
        self.playlist_id = playlist_id
        self.get_playlist_data()

    def get_playlist_data(self, playlist_url: str = None) -> None:
        """ Retrieve playlist form spotify """
        if not playlist_url:
            playlist_url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"

        json_data = self._auth.send_request(playlist_url)
        self.analyze_playlist_data(json_data)

        next_url = json_data['next']
        if next_url:
            self.get_playlist_data(next_url)

    def analyze_playlist_data(self, json_data: str) -> None:
        """ Stores data for each song in a SongData object. """
        for song in json_data['items']:
            song_data = SongData(song)
            self.song_list.append(song_data)

    def get_data_as_dict(self) -> list[dict]:
        song_list = []
        for song in self.song_list:
            song_list.append(song.get_data_as_dict())
        return song_list

    def get_data_as_csv(self) -> str:
        csv_str = "song_artist;song_name;album_artist;album_name;release_date;track_num;track_total;disc_num;disc_total"
        for song in self.song_list:
            csv_str += "\n" + song.get_data_as_csv()
        return csv_str

    def __str__(self) -> str:
        return str(self.song_list)


class SpotifyAuth:
    """ Class for authentication on spotify. """
    _api_token: str = None
    url = "https://accounts.spotify.com/api/token"

    def __init__(self) -> None:
        load_dotenv() # For testing
        self.get_token()
        self._headers = {
            "Authorization": "Bearer " + self._api_token
        }

    def get_token(self) -> None:
        """ Retrieve spotify api token. """
        # Retrieve ID and secret from .env
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

        # Authorization
        data = {}
        data['grant_type'] = "client_credentials"
        data['client_id'] = client_id
        data['client_secret'] = client_secret

        r = requests.post(self.url, data=data, timeout=10)

        if r is None:
            print("Spotify request timed out", file=sys.stderr)
            sys.exit(101)

        if r.status_code != 200:
            print(f"An error occured retrieving bearer token from spotify with status code: {r.status_code}", file=sys.stderr)
            print(f"{str(r.content)}", file=sys.stderr)
            sys.exit(102)

        out_json = r.json()

        if "error" in out_json:
            print("An error occured retrieving bearer token from spotify:", file=sys.stderr)
            print(out_json['error'] + ":", file=sys.stderr)
            if "error_description" in out_json:
                print(out_json['error_description'], file=sys.stderr)
            sys.exit(-1)

        self._api_token = out_json['access_token']

    def send_request(self, url: str) -> str:
        """ Send request to spotify api and return a json object. """
        res = requests.get(url=url, headers=self._headers, timeout=10)
        if res is None:
            print("Spotify request timed out", file=sys.stderr)
            sys.exit(101)

        return json.loads(res.content)
