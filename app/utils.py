from urllib2 import urlopen
import json

def extract_ytid(url):
    n = url.find('?v=')
    return url[n+3:n+3+11]

def get_video_data(ytid):
    try:
        raw_data = urlopen('https://gdata.youtube.com/feeds/api/videos/' + ytid + '?v=2&alt=jsonc').read()
    except:
        return None
    data = dict(json.loads(raw_data))
    return data['data']
