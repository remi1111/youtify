""" Executable functions for main.py """
import spotify_api
# import yt_api


def playlist_to_file(playlist):
    """ Turns a spotify playlist into a file.
        Dictionary of info is from get_playlist """
    token = spotify_api.get_token()
    mydict = spotify_api.get_playlist(playlist, token)
    spotify_api.write_to_file(mydict, "myplaylist.txt")
