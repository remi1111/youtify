""" Matching of titles artists and videos. """
from datetime import date
import string
import yt_api
import analyze

def string_clean(strs):
    """ Cleans a string to have only a-z and 0-9. """
    return strs \
            .split("(")[0] \
            .strip() \
            .lower() \
            .replace(" ","") \
            .translate(str.maketrans('', '', string.punctuation))

def get_songlist_artist(data, artist):
    """ Creates a list of songnames for an artist """
    songlist = []
    for song in data:
        if song['song artist'] == artist:
            songlist.append(string_clean(song['song name']))
    return songlist

def get_videoid_per_artist(artistchannelid, songlist, artist):
    """ Creates a dictionary of songs per artist. """
    ytdata = analyze.analyze_list(yt_api.get_video_list(yt_api.get_upload_list(artistchannelid)))
    dupedict = {}
    for song in ytdata:
        name = string_clean(song['song name'])
        if name in songlist:
            if yt_api.video_is_valid(song['videoid']):
                dat = date(int(song['published on'][0:4]),
                           int(song['published on'][5:7]),
                           int(song['published on'][8:10]))
                if name not in dupedict:
                    dupedict[name] = [dat, song['videoid'], artist, song['song name']]
                elif dat < dupedict[name][0] :
                    dupedict[name] = [dat, song['videoid'], artist, song['song name']]
    return dupedict

def songs_not_found(songlist, id_dict):
    """ Creates a list of songnames that were not found for an artist """
    not_found_list = []
    for song in songlist:
        if song not in id_dict.keys():
            not_found_list.append(song)
    return not_found_list
