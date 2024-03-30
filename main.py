""" Main Executable. """
import sys
import getopt
from dotenv import load_dotenv
import exec_func

def main():
    """ Main function. """
    load_dotenv() # Load .env file
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hFLD", ["help","to-file","to-list", "--to-dict"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err, file=sys.stderr)  # will print something like "option -a not recognized"
        usage()
        sys.exit(3)
    for opt, _ in opts:
        if opt in ("-h", "--help"): # Help message
            usage()
        elif opt in ("-F", "--to-file"):
            if len(args) != 2:
                print(f"{opt} requires 2 parameters", file=sys.stderr)
                sys.exit(3)
            exec_func.playlist_to_file(args[0], args[1])
        elif opt in ("-L", "--to-list"):
            if len(args) != 2:
                print(f"{opt} requires 2 parameters", file=sys.stderr)
                sys.exit(3)
            exec_func.playlist_to_yt_list(args[0], args[1])
        elif opt in ("-D", "--to-dict"):
            if len(args) != 2:
                print(f"{opt} requires 2 parameters", file=sys.stderr)
                sys.exit(3)
            exec_func.playlist_to_yt_dict(args[0], args[1])
        else:
            print("unhandled option", file=sys.stderr)
            sys.exit(-1)

def usage():
    """ Prints how to use the file. """
    print("-h, --help: Prints this message.")
    print("-F, --to-file <1> <2>: outputs spotify playlist <1> info to specified file <2>.")
    print("-L, --to-list <1> <2>: outputs spotify playlist <1> as a list of youtube video\
ID's to specified file <2>.")
    print("-D, --to-dict <1> <2>: outputs spotify playlist <1> as a dictionary of relevant\
info and their \n\t\t\t youtube video ID's to specified file <2>.")

if __name__ == "__main__":
    main()

    # PLAYLIST = "0hxTtbe3Kxll0hKBZR09LV"
    # test_playlist = "10GvxKrWBqtUDD8PtRUnsJ"

    # exec_func.playlist_to_file(PLAYLIST)
