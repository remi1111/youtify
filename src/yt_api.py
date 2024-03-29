""" Youtube API requests """
import requests
import json
import sys
import os

yt_api_key = os.getenv("YOUTUBE_API")

def api_call(page):
    """ Handles youtube API calls.
        Exits runtime upon failure.
        page: API call.
        returns: data from API call """
    data = requests.get(page)
    if data.status_code != 200:
        print(data.content)
        sys.exit(0)
    else:
        return data

def get_upload_list(channel_id):
    data = api_call("https://www.googleapis.com/youtube/v3/channels?id=" + channel_id + "&key=" + yt_api_key + "&part=contentDetails,statistics").content
    video_count = json.loads(data)["items"][0]["statistics"]["videoCount"]
    print("videos: " + video_count)
    return json.loads(data)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_video_list(playlist_id, video_array=[], page_token=None):
    if(page_token):
        data = api_call("https://www.googleapis.com/youtube/v3/playlistItems?playlistId=" + playlist_id + "&key=" + yt_api_key + "&part=snippet&maxResults=50&regionCode=nl&pageToken=" + page_token).content
    else:
        data = api_call("https://www.googleapis.com/youtube/v3/playlistItems?playlistId=" + playlist_id + "&key=" + yt_api_key + "&part=snippet&maxResults=50&regionCode=nl").content
    new_array = video_array + json.loads(data)["items"]
    try:
        page_token = json.loads(data)["nextPageToken"]
    except:
        return new_array
    return get_video_list(playlist_id, new_array, page_token)

def get_playlist_by_channel(channel_id):
    data = api_call("https://youtube.googleapis.com/youtube/v3/playlists?part=snippet%2CcontentDetails&channelId="+ channel_id +"&maxResults=50&key=" + yt_api_key).content
    # print(data)

def get_id_from_playlist(playlist_id):
    data = api_call("https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails,snippet,id&playlistId=" + playlist_id + "&key=" + yt_api_key).content
    # print(data)


def video_is_valid(videoid):
    data = api_call("https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&regionCode=NL&id=" + videoid + "&key=" + yt_api_key)
    jsondat = json.loads(data.content)
    cont = jsondat['items'][0]['contentDetails']
    if 'regionRestriction' in cont:
        if 'allowed' in cont['regionRestriction'] and 'NL' not in cont['regionRestriction']['allowed']:
            return 0
        if 'blocked' in cont['regionRestriction'] and 'NL' in cont['regionRestriction']['blocked']:
            return 0
    return 1

def return_blocked(videoid):
    data = api_call("https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&regionCode=NL&id=" + videoid + "&key=" + yt_api_key)
    jsondat = json.loads(data.content)
    cont = jsondat['items'][0]['contentDetails']
    if 'regionRestriction' in cont:
        if 'allowed' in cont['regionRestriction']:
            print("allowed")
            print(cont['regionRestriction']['allowed'])
        if 'blocked' in cont['regionRestriction']:
            print("blocked")
            print(cont['regionRestriction']['blocked'])
    return 0

def search_channel(channel):
    data = api_call("https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q=" + channel + "&key=" + yt_api_key)
    # print(json.loads(data.content))
    return json.loads(data.content)['items'][0]['id']['channelId']

def video_is_valid_and_statistics(videoid):
    data = api_call("https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&regionCode=NL&id=" + videoid + "&key=" + yt_api_key)
    jsondat = json.loads(data.content)
    print(jsondat)
    cont = jsondat['items'][0]['contentDetails']
    Vcount = jsondat['items'][0]['statistics']['viewCount']
    if 'regionRestriction' in cont:
        if 'allowed' in cont['regionRestriction'] and 'NL' not in cont['regionRestriction']['allowed']:
            return [0, Vcount]
        if 'blocked' in cont['regionRestriction'] and 'NL' in cont['regionRestriction']['blocked']:
            return [0, Vcount]
    return [1, Vcount]

