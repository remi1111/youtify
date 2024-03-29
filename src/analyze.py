""" Analyzing results from API calls. """

def analyze_list(json_list):
    """ Analyzing JSON result from youtube api call.
        Returns all songs in a dictionary. """
    count = 0
    test = 0
    mylist = []
    for item in json_list:
        count += 1
        title = item["snippet"]["title"]
        if 'korean version' in title.lower():
            test += 1
        elif 'full version' in title.lower():
            test += 1
        elif 'remix' in title.lower():
            continue
        elif '(inst.)' in title.lower():
            continue
        elif '(inst)' in title.lower():
            continue
        elif '(instrumental)' in title.lower():
            continue
        elif 'version' in title.lower():
            continue
        elif 'ver.' in title.lower():
            continue
        channel = item["snippet"]["channelTitle"]
        videoid = item["snippet"]["resourceId"]["videoId"]
        ytlink = "www.youtube.com/watch?v=" + videoid
        # print(title + " by " + channel + ": youtube.com/watch?v=" + videoid)
        descrip = item["snippet"]["description"]
        publishedon = item['snippet']["publishedAt"]
        try:
            splitted = descrip.split("Released on: ")[1][0:10]
            released_on = splitted
            mydict = {'song name': title,
                      'artist name': channel,
                      'videoid': videoid,
                      "ytlink": ytlink,
                      'published on': publishedon,
                      'release date': released_on}
        except IndexError:
            mydict = {'song name': title,
                      'artist name': channel,
                      'videoid': videoid,
                      "ytlink": ytlink,
                      'published on': publishedon}
        mylist.append(mydict)
    # print(count)
    return mylist
