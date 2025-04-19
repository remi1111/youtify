""" Main Executable. """
import sys
import os
import getopt
from dotenv import load_dotenv
from src import exec_func

def main():
    """ Main function. """
    load_dotenv() # Load .env file
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                    "hFLDvf",
                                    ["help", "to-file",
                                     "to-list", "--to-dict",
                                     "--verbose", "--full"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err, file=sys.stderr)  # will print something like "option -a not recognized"
        usage()
        sys.exit(3)
    if opts is None:
        usage()
        sys.exit(0)
    for opt, _ in opts:
        match opt:
            case "-h" | "--help":
                usage()
                sys.exit(0)
            case "-v" | "--verbose":
                os.environ["VERBOSE"] = "1"
            case "-F" | "--to-file":
                if len(args) != 2:
                    print(f"{opt} requires 2 parameters", file=sys.stderr)
                    sys.exit(3)
                exec_func.playlist_to_file(args[0], args[1])
            case "-L" | "--to-list":
                if len(args) != 2:
                    print(f"{opt} requires 2 parameters", file=sys.stderr)
                    sys.exit(3)
                exec_func.playlist_to_yt_list(args[0], args[1])
            case "-D" | "--to-dict":
                if len(args) != 2:
                    print(f"{opt} requires 2 parameters", file=sys.stderr)
                    sys.exit(3)
                exec_func.playlist_to_yt_dict(args[0], args[1])
            case "-f" | "--full":
                if len(args) != 1:
                    print(f"{opt} requires 1 parameter", file=sys.stderr)
                    sys.exit(3)
                exec_func.full(args[0])
            case _:
                print("unhandled option", file=sys.stderr)
                sys.exit(-1)

def usage():
    """ Prints how to use the file. """
    print("-h, --help: Prints this message.")
    print("-v, --verbose: Prints important output during runtime.")
    print("-F, --to-file <1> <2>: outputs spotify playlist <1> info to specified file <2>.")
    print("-L, --to-list <1> <2>: outputs spotify playlist <1> as a list of youtube video \
ID's to specified file <2>.")
    print("-D, --to-dict <1> <2>: outputs spotify playlist <1> as a dictionary of relevant \
info and their \n\t\t\t youtube video ID's to specified file <2>.")
    print("-f, --full <1>: Download audio files for all songs in \
spotify playlist <1> \n\t\t\t and put them in the audio folder.")

if __name__ == "__main__":
    main()

    # PLAYLIST = "0hxTtbe3Kxll0hKBZR09LV"
    # test_playlist = "10GvxKrWBqtUDD8PtRUnsJ"

    # exec_func.playlist_to_file(PLAYLIST)
