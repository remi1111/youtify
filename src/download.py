""" Downloading of songs through yt-dlp """
import subprocess

def download_ids(id_dict, verbose=False):
    """ Download all songs from a dictionary. """
    for song in id_dict:
        title =  "~/audio/" + song['song artist'] + " - " + song['song name'] + ".%(ext)s"
        page = "https://www.youtube.com/watch?v=" + song['video id']
        if verbose:
            print(song['song name']  + "\t id:  " + song['video id'])
        subprocess.run(["yt-dlp",
                        '-x',
                        '-f',
                        'ba',
                        '--audio-format',
                        'mp3',
                        '-o',
                        title,
                        page],
                        check=False)

def download_1(artist, song, vid_id):
    """ Download 1 song with artist and song as parameters. """
    title =  "~/audio/" + artist + " - " + song + ".%(ext)s"
    page = "https://www.youtube.com/watch?v=" + vid_id
    subprocess.run(["yt-dlp",
                    '-x',
                    '-f',
                    'ba',
                    '--audio-format',
                    'mp3',
                    '-o',
                    title,
                    page],
                    check=False)

def download_1_fast(vid_id):
    """ Download 1 song with just the video id. """
    title =  "~/audio/%(uploader)s - %(title)s.%(ext)s"
    page = "https://www.youtube.com/watch?v=" + vid_id
    subprocess.run(["yt-dlp",
                    '-x',
                    '-f',
                    'ba',
                    '--audio-format',
                    'mp3',
                    '-o',
                    title,
                    page],
                    check=False)

# def playlist_download(playlist_id):
#     id_list = []
#     return id_list

def download_id_list(id_list):
    """ Download all songs from a list of video ids. """
    for video_id in id_list:
        title =  "~/audio/%(uploader)s - %(title)s.%(ext)s"
        page = "https://www.youtube.com/watch?v=" + video_id
        subprocess.run(["yt-dlp",
                        '-x',
                        '-f',
                        'ba',
                        '--audio-format',
                        'mp3',
                        '-o',
                        title,
                        page],
                        check=False)
