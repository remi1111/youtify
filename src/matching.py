""" Matching of titles artists and videos. """
import string

def string_clean(strs):
    """ Cleans a string to have only a-z and 0-9. """
    return strs \
            .split("(")[0] \
            .strip() \
            .lower() \
            .replace(" ","") \
            .translate(str.maketrans('', '', string.punctuation))

def compare_string(str1, str2):
    """ Compares 2 strings. """
    return string_clean(str1) == string_clean(str2)
