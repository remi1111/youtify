""" Executable functions for main.py """
import spotify_api
# import yt_api


def playlist_to_file(playlist, filename):
    """ Turns a spotify playlist into a file.
        Dictionary of info is from get_playlist """
    token = spotify_api.get_token()
    mydict = spotify_api.get_playlist(playlist, token, [])
    spotify_api.write_to_file(mydict, filename)

def playlist_to_yt_list(playlist, filename=None):
    """ Turns a spotify playlist into a list of youtube video ids.
        If no filename is given print to console. """

def playlist_to_yt_dict(playlist, filename=None):
    """ Turns a spotify playlist into a dictionary.
        This dictionary contains relevant info and their youtube ids.
        If no filename is given print to console. """
