""" Main Executable. """
from dotenv import load_dotenv
import exec_func

if __name__ == "__main__":
    load_dotenv() # Load .env file
    PLAYLIST = "0hxTtbe3Kxll0hKBZR09LV"

    exec_func.playlist_to_file(PLAYLIST)
