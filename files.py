import urllib
import urllib2
import os

#Constants
REFRESH = False # if set to False: do not  download files (if they are already downloaded)
XML_PATH = "./xml/"


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def dowload_url (url, fileName):
    """Downloads URL into a local file"""

    ensure_dir(XML_PATH)
    fileComplete = XML_PATH + fileName

    #load data if refresh is on or file does not exist
    if (REFRESH) or not (os.path.exists(fileComplete)):
        ads_data = urllib2.urlopen(url)
        html = ads_data.read()
        fh = open(fileComplete, "w")
        fh.write(html)
        fh.close()
