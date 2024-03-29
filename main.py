# Main executable.
import sys
sys.path.insert(1, "/home/remco/Documents/youtify/src")

from dotenv import load_dotenv
import spotify_api

if __name__ == "__main__":
    load_dotenv() # Load .env file
    token = spotify_api.get_token()
    download_playlist = "7wD6vwNMh1LHExbQBVZPtp"
    mydict = spotify_api.get_playlist(download_playlist, token)
    spotify_api.write_to_file(mydict, "myplaylist.txt")
