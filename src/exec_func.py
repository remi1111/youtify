""" Executable functions for main.py """
import json
import os
import sys

from src.spotify_api import SpotifyPlaylistData
from src import get_avs
from src import download
from src import metadata
# import yt_api


class ExecFunc:
    spotify_playlist_data: SpotifyPlaylistData = None

    def __init__(self, playlist_id=None) -> None:
        if playlist_id:
            self.spotify_playlist_data = SpotifyPlaylistData(playlist_id)
        else:
            print("playlist id requried")
            sys.exit(3)

    def write_to_file_as_dict(self, filename: str) -> None:
        """ Write a playlist dictionary to a file. """
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(json.dumps(self.spotify_playlist_data.get_data_as_dict()))

    def write_to_file_as_csv(self, filename: str) -> None:
        """ Write a playlist dictionary to a file. """
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(json.dumps(self.spotify_playlist_data.get_data_as_csv()))

    def get_spotify_playlist_data(self, playlist_id: str) -> None:
        self.spotify_playlist_data = SpotifyPlaylistData(playlist_id)

    def playlist_to_yt_list(self) -> list:
        """ Turns a spotify playlist into a list of youtube video ids.
            If no filename is given print to console. """
        verbose = False
        if os.environ["VERBOSE"] == "1":
            verbose = True
        return get_avs.get_dict_spotify(self.spotify_playlist_data, verbose)

    def playlist_to_yt_dict(self) -> dict:
        """ Turns a spotify playlist into a dictionary.
            This dictionary contains relevant info and their youtube ids.
            If no filename is given print to console. """
        pass

    def full(self) -> None:
        """ Downloads and tags all songs from a spotify playlist. """
        verbose = False
        if os.environ["VERBOSE"] == "1":
            verbose = True

        mydict = get_avs.get_dict_spotify(self.spotify_playlist_data, verbose)
        download.download_ids(mydict, verbose)
        metadata.tag_all(mydict)
