# To download songs through yt-dlp
import subprocess

def download_ids(id_dict):
    for song in id_dict:
        title =  "~/audio/" + id_dict[song][2] + " - " + id_dict[song][3] + ".%(ext)s"
        page = "https://www.youtube.com/watch?v=" + id_dict[song][1]
        print(id_dict[song][3]  + "\t id:  " + id_dict[song][1])
        subprocess.run(["yt-dlp", '-x', '-f', 'ba','--audio-format', 'mp3', '-o', title, page])

def download_1(artist, song, id):
    title =  "~/audio/" + artist + " - " + song + ".%(ext)s"
    page = "https://www.youtube.com/watch?v=" + id
    subprocess.run(["yt-dlp", '-x', '-f', 'ba','--audio-format', 'mp3', '-o', title, page])

def download_1_fast(id):
    title =  "~/audio/%(uploader)s - %(title)s.%(ext)s"
    page = "https://www.youtube.com/watch?v=" + id
    subprocess.run(["yt-dlp", '-x', '-f', 'ba','--audio-format', 'mp3', '-o', title, page])

def playlist_download(playlist_id):
    id_list = []
    return id_list

def download_id_list(id_list):
    for video_id in id_list:
        title =  "~/audio/%(uploader)s - %(title)s.%(ext)s"
        page = "https://www.youtube.com/watch?v=" + video_id
        subprocess.run(["yt-dlp", '-x', '-f', 'ba','--audio-format', 'mp3', '-o', title, page])
