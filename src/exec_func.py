""" Executable functions for main.py """
import json

import spotify_api
import get_avs
# import yt_api

def write_to_file(song_dict, filename):
    """ Write a playlist dictionary to a file. """
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(json.dumps(song_dict))

def playlist_to_file(playlist, filename=None):
    """ Turns a spotify playlist into a file.
        Dictionary of info is from get_playlist """
    token = spotify_api.get_token()
    mydict = spotify_api.get_playlist(playlist, token, [])
    if filename:
        write_to_file(mydict, filename)
    else:
        print(mydict)

def playlist_to_yt_list(playlist, filename=None):
    """ Turns a spotify playlist into a list of youtube video ids.
        If no filename is given print to console. """
    token = spotify_api.get_token()
    mydict = spotify_api.get_playlist(playlist, token, [])
    if filename:
        write_to_file(mydict, filename)
    else:
        print(mydict)

def playlist_to_yt_dict(playlist, filename=None):
    """ Turns a spotify playlist into a dictionary.
        This dictionary contains relevant info and their youtube ids.
        If no filename is given print to console. """
    token = spotify_api.get_token()
    dict1 = spotify_api.get_playlist(playlist, token, [])
    mydict = get_avs.get_dict_spotify(dict1)
    if filename:
        write_to_file(mydict, filename)
    else:
        print(mydict)
