""" Youtube API requests """
import json
import sys
import os
from typing import Any

import requests
from requests import Response


class YoutubeApi:
    yt_api_key = None
    base_url = "https://www.googleapis.com/youtube/v3/"

    def __init__(self) -> None:
        self.yt_api_key = os.getenv("YOUTUBE_API")
        self.region = os.getenv("REGION_CODE")
        self.verbose = True if os.getenv("VERBOSE") == 1 else False

    def api_call(self, url: str) -> Response:
        """ Handles youtube API calls.
            Exits runtime upon failure.
            url: API call.
            returns: data from API call """
        url += f"&key={self.yt_api_key}"
        data = requests.get(url, timeout=10)
        if data is None:
            print("Youtube request timed out", file=sys.stderr)
            sys.exit(101)

        if data.status_code != 200:
            print("Youtube request not successfull", file=sys.stderr)
            print(data.content, file=sys.stderr)
            sys.exit(501)
        else:
            return data

    @staticmethod
    def user_channel_check(channel_id: str) -> None:
        if channel_id[:2] != "UC":
            print("Channel ID did not start with UC", file=sys.stderr)
            sys.exit(1)

    def get_upload_list(self, channel_id: str) -> str:
        """ Retrieves user uploads from user channel. """
        self.user_channel_check(channel_id)
        s = list(channel_id)
        s[1] = "U"
        return "".join(s)

    def get_upload_list_call(self, channel_id: str) -> str:
        """ Api call for channel to user uploads. """
        self.user_channel_check(channel_id)
        url = f"{self.base_url}channels?id={channel_id}&part=contentDetails,statistics"
        data = self.api_call(url).content

        if self.verbose:
            video_count = json.loads(data)["items"][0]["statistics"]["videoCount"]
            print("videos: " + video_count)
        return json.loads(data)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    def get_video_list(self, playlist_id: str, video_array: list, page_token: str = None) -> list:
        """ Retrieves a list of videos from a youtube playlist. """
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&part=snippet&maxResults=50&regionCode={self.region}"
        if page_token:
            url += f"&pageToken={page_token}"
        data = self.api_call(url).content

        new_array = video_array + json.loads(data)["items"]

        try:
            page_token = json.loads(data)["nextPageToken"]
        except KeyError:
            return new_array

        return self.get_video_list(playlist_id, new_array, page_token)

    def get_playlist_by_channel(self, channel_id: str) -> bytes:
        """ Retrievs all playlists of a channel. """
        url = f"{self.base_url}playlists?part=snippet%2CcontentDetails&channelId={channel_id}&maxResults=50"
        return self.api_call(url).content

    def get_id_from_playlist(self, playlist_id: str) -> bytes:
        """ No idea """
        url = f"{self.base_url}playlistItems?part=contentDetails,snippet,id&playlistId={playlist_id}"
        return self.api_call(url).content

    def get_region_restrictions(self, videoid: str) -> dict:
        """ Prints a list of allowed or blocked countries. """
        url = f"{self.base_url}videos?part=contentDetails&regionCode={self.region}&id={videoid}"
        data = self.api_call(url)
        jsondat = json.loads(data.content)
        cont = jsondat['items'][0]['contentDetails']
        if 'regionRestriction' in cont:
            return cont['regionRestriction']
        return {}

    def video_is_valid(self, videoid: str) -> bool:
        """ Return a boolean if the video is valid in a country. """
        cont = self.get_region_restrictions(videoid)
        if 'regionRestriction' in cont:
            if('allowed' in cont['regionRestriction'] and
            self.region not in cont['regionRestriction']['allowed']):
                return False
            if('blocked' in cont['regionRestriction'] and
            self.region in cont['regionRestriction']['blocked']):
                return False
        return True

    def get_topic_channel(self, json_data: Any) -> str:
        """ Takes first channel with topic in the name. """
        for item in json_data:
            channel_name = item['snippet']['channelTitle']
            if self.verbose:
                print(channel_name)
            if "Topic" in channel_name:
                return item['id']['channelId']
        print("Could not find topic channel", file=sys.stderr)
        sys.exit(10)

    def search_channel(self, channel_name: str) -> str:
        """ Returns the channel ID of the first result. """
        url = f"{self.base_url}search?part=snippet&type=channel&q={channel_name}"
        data = self.api_call(url)
        channel_id = self.get_topic_channel(json.loads(data.content)['items'])

        if self.verbose:
            print(f"Channel ID: {channel_id}")
            print(json.loads(data.content))

        return channel_id

    def video_is_valid_and_statistics(self, videoid: str) -> list[bool, int]:
        """ Returns a tuple of if a video is valid and its viewcount. """
        url = f"{self.base_url}videos?part=contentDetails&regionCode={self.region}&id={videoid}"
        data = self.api_call(url)
        jsondat = json.loads(data.content)

        if self.verbose:
            print(jsondat)

        cont = jsondat['items'][0]['contentDetails']
        view_count = jsondat['items'][0]['statistics']['viewCount']

        if 'regionRestriction' in cont:
            if('allowed' in cont['regionRestriction'] and
            self.region not in cont['regionRestriction']['allowed']):
                return [False, view_count]
            if('blocked' in cont['regionRestriction'] and
            self.region in cont['regionRestriction']['blocked']):
                return [False, view_count]
        return [True, view_count]
