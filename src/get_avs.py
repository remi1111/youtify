""" Retrieve information from youtube. """
import yt_api
import analyze

def get_dict_channel(channel_id):
    """ Get dictionary of info for each song from a channel"""
    video_list = yt_api.get_video_list(yt_api.get_upload_list(channel_id), [])
    artist = video_list[0]['snippet']['channelTitle'].replace(" - Topic", "")
    print(artist)
    songlist = []

    for song in video_list:
        songtitle = song['snippet']['title']
        upload_date = song['snippet']['publishedAt']
        video_id = song['snippet']['resourceId']['videoId']
        desc = song['snippet']['description']
        try:
            release_date = desc.split("Released on: ")[1].split("\n")[0]
        except KeyError:
            release_date = "N/A"
        [valid, views] = yt_api.video_is_valid_and_statistics(video_id)
        if valid:
            song_dict = {'artist': artist,
                            'title': songtitle,
                            'upload_date': upload_date,
                            'release_date': release_date,
                            'video_id': video_id,
                            'views':views}
            songlist.append(song_dict)
    return songlist

def get_dict_spotify(mydict, verbose=False):
    """ Get dictionary of info from a
        spotify playlist through youtube"""

    # order by artists
    set_artists = set()
    for song in mydict:
        set_artists.add(song['song artist'])

    if verbose:
        count_artists = len(set_artists)
        print(f"Artists: {count_artists}")

    for artist in set_artists:
        songlist = analyze.get_clean_songlist_artist(mydict, artist)
        spotify_dict = analyze.get_dict_artist(mydict, artist)

        artistchannel = artist + " - Topic"
        channelid = yt_api.search_channel(artistchannel, verbose)

        yt_data = analyze.get_videoid_dict_per_artist(channelid,
                                                      songlist,
                                                      spotify_dict,
                                                      artist,
                                                      verbose)

        not_found_list = analyze.songs_not_found(songlist, yt_data)

        count = len(songlist)
        found = len(songlist) - len(not_found_list)


        if verbose:
            print(f"Artist: {artist}")
            print("count = " + str(count) + ",  found = " + str(found))
            print("not found:", not_found_list)

    return yt_data
