import urllib.request as req
from urllib.parse import urlparse

def download(url, to=None):
    if check_url(url):
        if(to == None):
            local_filename = req.urlretrieve(url, './' + url.split('/')[-1])
        else:
            local_filename = req.urlretrieve(url, to)
        return local_filename[0]
    else:
        return "No URL"

def check_url(url):
    urlResult = urlparse(url)
    if urlResult.scheme and urlResult.netloc and urlResult.path:
        return True
    return False