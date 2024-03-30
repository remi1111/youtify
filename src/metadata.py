""" File for adding metadata to downloaded files"""
import eyed3

def tag_file(filename, mydict, genre):
    """ Tags a song with info from mydict. """
    audiofile = eyed3.load(filename)

    audiofile.tag.artist = mydict['song artist']
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

def tag_all(mydict, verbose=False):
    """ Tags all songs in mydict. """
    for key in mydict:
        song = mydict[key]
        if verbose:
            print(song)
        filename =  "./audio/" + song['song artist'] + " - " + song['song name youtube'] + ".mp3"
        tag_file(filename, song, "K-pop")
