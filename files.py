import urllib
import urllib2

xml_path = "./xml/"

def dowload_url (url, fileName):

    #print url
    ads_data = urllib2.urlopen(url)

    # Get all data
    #print "Retrieving data from ADS..."
    html = ads_data.read()

    #open the fileName for writing
    print "Writing file " + fileName
    fh = open(xml_path + fileName, "w")

    fh.write(html)

    fh.close()

    #print "Finished"
