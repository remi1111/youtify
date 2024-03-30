""" Youtube API requests """
import json
import sys
import os

import requests

def api_call(page):
    """ Handles youtube API calls.
        Exits runtime upon failure.
        page: API call.
        returns: data from API call """
    data = requests.get(page, timeout=10)
    if data is None:
        print("Youtube request timed out", file=sys.stderr)
        sys.exit(101)

    if data.status_code != 200:
        print("Youtube request not successfull", file=sys.stderr)
        print(data.content, file=sys.stderr)
        sys.exit(501)
    else:
        return data

def get_upload_list(channel_id):
    """ Quick channel to user uploads. """
    if channel_id[:2] != "UC":
        print("Channel ID did not start with UC", file=sys.stderr)
        sys.exit(1)
    s = list(channel_id)[1] = "U"
    return "".join(s)

def get_upload_list_call(channel_id, verbose=False):
    """ Api call for channel to user uploads. """
    if channel_id[:2] != "UC":
        print("Channel ID did not start with UC", file=sys.stderr)
        sys.exit(1)
    yt_api_key = os.getenv("YOUTUBE_API")
    data = api_call("https://www.googleapis.com/youtube/v3/channels?id=" +
                    channel_id + "&key=" +
                    yt_api_key + "&part=contentDetails,statistics").content

    if verbose:
        video_count = json.loads(data)["items"][0]["statistics"]["videoCount"]
        print("videos: " + video_count)
    return json.loads(data)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_video_list(playlist_id, video_array, page_token=None):
    """ Retrieves a list of videos from a youtube playlist. """
    yt_api_key = os.getenv("YOUTUBE_API")
    if page_token:
        data = api_call("https://www.googleapis.com/youtube/v3/playlistItems?playlistId=" +
                        playlist_id + "&key=" + yt_api_key +
                        "&part=snippet&maxResults=50&regionCode=nl&pageToken=" +
                        page_token).content
    else:
        data = api_call("https://www.googleapis.com/youtube/v3/playlistItems?playlistId=" +
                        playlist_id + "&key=" + yt_api_key +
                        "&part=snippet&maxResults=50&regionCode=nl").content

    new_array = video_array + json.loads(data)["items"]

    try:
        page_token = json.loads(data)["nextPageToken"]
    except KeyError:
        return new_array

    return get_video_list(playlist_id, new_array, page_token)

def get_playlist_by_channel(channel_id):
    """ Retrievs all playlists of a channel. """
    yt_api_key = os.getenv("YOUTUBE_API")
    data = api_call("https://youtube.googleapis.com/youtube/v3/" +
                    "playlists?part=snippet%2CcontentDetails&channelId=" +
                    channel_id +"&maxResults=50&key=" + yt_api_key).content
    return data

def get_id_from_playlist(playlist_id):
    """ No idea """
    yt_api_key = os.getenv("YOUTUBE_API")
    data = api_call("https://www.googleapis.com/youtube/v3/" +
                    "playlistItems?part=contentDetails,snippet,id&playlistId=" +
                    playlist_id + "&key=" + yt_api_key).content
    return data


def video_is_valid(videoid):
    """ Return a boolean if the video is valid in a country. """
    yt_api_key = os.getenv("YOUTUBE_API")
    data = api_call("https://youtube.googleapis.com/youtube/v3/" +
                    "videos?part=contentDetails&regionCode=NL&id=" +
                    videoid + "&key=" + yt_api_key)
    jsondat = json.loads(data.content)
    cont = jsondat['items'][0]['contentDetails']
    if 'regionRestriction' in cont:
        if('allowed' in cont['regionRestriction'] and
           'NL' not in cont['regionRestriction']['allowed']):
            return False
        if('blocked' in cont['regionRestriction'] and
           'NL' in cont['regionRestriction']['blocked']):
            return False
    return True

def return_blocked(videoid):
    """ Prints a list of allowed or blocked countries. """
    yt_api_key = os.getenv("YOUTUBE_API")
    data = api_call("https://youtube.googleapis.com/youtube/v3/" +
                    "videos?part=contentDetails&regionCode=NL&id=" +
                    videoid + "&key=" + yt_api_key)
    jsondat = json.loads(data.content)
    cont = jsondat['items'][0]['contentDetails']
    if 'regionRestriction' in cont:
        if 'allowed' in cont['regionRestriction']:
            print("allowed")
            print(cont['regionRestriction']['allowed'])
        if 'blocked' in cont['regionRestriction']:
            print("blocked")
            print(cont['regionRestriction']['blocked'])
    return False

def take_topic(json_data, verbose=False):
    """ Takes first channel with topic in the name. """
    for item in json_data:
        channel_name = item['snippet']['channelTitle']
        if verbose:
            print(channel_name)
        if "Topic" in channel_name:
            return item['id']['channelId']

def search_channel(channel_name, verbose=False):
    """ Returns the channel ID of the first result. """
    yt_api_key = os.getenv("YOUTUBE_API")
    data = api_call("https://www.googleapis.com/youtube/v3/" +
                    "search?part=snippet&type=channel&q=" +
                    channel_name + "&key=" + yt_api_key)
    channel_id = take_topic(json.loads(data.content)['items'], verbose)
    if verbose:
        print(f"Channel ID: {channel_id}")
        print(json.loads(data.content))

    return channel_id

def video_is_valid_and_statistics(videoid, verbose=False):
    """ Returns a tuple of if a video is valid and its viewcount. """
    yt_api_key = os.getenv("YOUTUBE_API")
    data = api_call("https://youtube.googleapis.com/youtube/v3/" +
                    "videos?part=contentDetails,statistics&regionCode=NL&id=" +
                    videoid + "&key=" + yt_api_key)
    jsondat = json.loads(data.content)

    if verbose:
        print(jsondat)

    cont = jsondat['items'][0]['contentDetails']
    view_count = jsondat['items'][0]['statistics']['viewCount']

    if 'regionRestriction' in cont:
        if('allowed' in cont['regionRestriction'] and
           'NL' not in cont['regionRestriction']['allowed']):
            return [False, view_count]
        if('blocked' in cont['regionRestriction'] and
           'NL' in cont['regionRestriction']['blocked']):
            return [False, view_count]
    return [True, view_count]
