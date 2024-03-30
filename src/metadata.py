""" File for adding metadata to downloaded files"""
import eyed3

def tag_file(filename, mydict, genre):
    audiofile = eyed3.load(filename)

    audiofile.tag.artist = mydict['artist name']
    audiofile.tag.album = mydict['album name']
    audiofile.tag.album_artist = mydict['album artist']
    audiofile.tag.title = mydict['song name spotify']
    audiofile.tag.recording_date = mydict['release year']
    audiofile.tag.track_num = mydict['track num']
    audiofile.tag.track_total = mydict['track total']
    audiofile.tag.disc_num = mydict['disc num']
    audiofile.tag.disc_total = mydict['disc total']
    audiofile.tag.genre = genre

    audiofile.tag.save()


if __name__ == "__main__":
    filename = "./audio/YOUNG POSSE - ROTY.mp3"
    mydict = {'artist name': 'YOUNG POSSE',
              'album name': 'XXL EP',
              'album artist': 'YOUNG POSSE',
              'song name spotify': 'ROTY',
              'release year': '2024',
              'track num': '4',
              'track total': '5',
              'disc num': '1',
              'disc total': '1'}
    genre = "K-pop"
    tag_file(filename, mydict, genre)
