""" Analyzing results from API calls. """
from datetime import date

import matching
import yt_api

def analyze_list(json_list):
    """ Analyzing JSON result from youtube api call.
        Returns all songs in a dictionary. """
    count = 0
    test = 0
    mylist = []
    for item in json_list:
        count += 1
        orig_title = item["snippet"]["title"]
        title = item["snippet"]["title"].lower()
        if 'korean version' in title:
            test += 1
        elif 'full version' in title:
            test += 1
        elif 'remix' in title:
            continue
        elif '(inst.)' in title:
            continue
        elif '(inst)' in title:
            continue
        elif '(instrumental)' in title:
            continue
        elif 'version' in title:
            continue
        elif 'ver.' in title:
            continue
        channel = item["snippet"]["channelTitle"]
        videoid = item["snippet"]["resourceId"]["videoId"]
        ytlink = "www.youtube.com/watch?v=" + videoid
        # print(title + " by " + channel + ": youtube.com/watch?v=" + videoid)
        descrip = item["snippet"]["description"]
        publishedon = item['snippet']["publishedAt"]
        try:
            splitted = descrip.split("Released on: ")[1][0:10]
            released_on = splitted
            mydict = {'song name': orig_title,
                      'artist name': channel,
                      'videoid': videoid,
                      "ytlink": ytlink,
                      'published on': publishedon,
                      'release date': released_on}
        except IndexError:
            mydict = {'song name': orig_title,
                      'artist name': channel,
                      'videoid': videoid,
                      "ytlink": ytlink,
                      'published on': publishedon}
        mylist.append(mydict)
    # print(count)
    return mylist

def get_songlist_artist(data, artist):
    """ Creates a list of songnames for an artist """
    songlist = []
    for song in data:
        if song['song artist'] == artist:
            songlist.append(matching.string_clean(song['song name']))
    return songlist

def str_date(strng):
    """ Transforms a string to date object. """
    obj = date(int(strng[0:4]),
                int(strng[5:7]),
                int(strng[8:10]))
    return obj

def get_videoid_per_artist(artistchannelid, songlist, artist):
    """ Creates a dictionary of songs per artist. """
    ytdata = analyze_list(yt_api.get_video_list(yt_api.get_upload_list(artistchannelid),[]))
    dupedict = {}
    for song in ytdata:
        name = matching.string_clean(song['song name'])
        if name in songlist:
            if yt_api.video_is_valid(song['videoid']):
                dat = str_date(song['published on'])
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
