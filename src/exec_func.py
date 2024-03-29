# All functions that can be executed from main.py
import spotify_api
import yt_api


def playlist_to_file(playlist):
    token = spotify_api.get_token()
    mydict = spotify_api.get_playlist(playlist, token)
    spotify_api.write_to_file(mydict, "myplaylist.txt")
