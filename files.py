import urllib
import urllib2

#Constants
REFRESH = False # if set to False: do not  download files (if they are already downloaded)
XML_PATH = "./xml/"

def dowload_url (url, fileName):
    """Downloads URL into a local file"""

    if REFRESH == True:
        #TODO: check if directory exists and if not create it
        ads_data = urllib2.urlopen(url)

        # Get all data
        #print "Retrieving data from ADS"
        print ">>> Downloading: " + url
        html = ads_data.read()

        #open the fileName for writing
        #print "Writing file " + XML_PATH + fileName
        fh = open(XML_PATH + fileName, "w")

        fh.write(html)

        fh.close()

        #print "Finished"
    else:
        print ">>> Skipping download: " + url
