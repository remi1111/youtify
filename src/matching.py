""" Matching of titles artists and videos. """

import yt_api
from datetime import *
import string

def get_songlist_artist(data, artist):
    songlist = []
    for song in data:
        if song['song artist'] == artist:
            songlist.append(song['song name'].split("(")[0].strip().lower().replace(" ","").translate(str.maketrans('', '', string.punctuation)))
    return songlist

def get_videoid_per_artist(artistchannelid, songlist, artist):
    ytdata = yt_api.analyze_list(yt_api.get_video_list(yt_api.get_upload_list(artistchannelid)))
    dupedict = {}
    for song in ytdata:
        name = song['song name'].split("(")[0].strip().lower().replace(" ","").translate(str.maketrans('', '', string.punctuation))
        if name in songlist:
            if yt_api.video_is_valid(song['videoid']):
                dat = date(int(song['published on'][0:4]), int(song['published on'][5:7]), int(song['published on'][8:10]))
                if name not in dupedict:
                    dupedict[name] = [dat, song['videoid'], artist, song['song name']]
                elif dat < dupedict[name][0] :
                    dupedict[name] = [dat, song['videoid'], artist, song['song name']]
    return dupedict

def songs_not_found(songlist, id_dict):
    not_found_list = []
    for song in songlist:
        if song not in id_dict.keys():
            not_found_list.append(song)
    return not_found_list
