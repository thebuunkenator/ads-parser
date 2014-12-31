import urllib2
import os
import xml.etree.ElementTree as ET

## Parse XML
def parse_xml (fileName):

    print
    print "Parsing XML: " + fileName
    tree = ET.parse(fileName)
    root = tree.getroot()


    print root.tag
    print root.attrib

    # for country in root:
    #     print country.attrib
    #
    #     rank = country.find('rank').text
    #     name = country.get('name').text
    #     print "name: " +  name
    #     print "rank: " + rank
    #
    #     for neighbor in root.iter('neighbor'):
    #         print neighbor.attrib


    for record in root:


        print
        title = record.find('title').text.encode('utf-8')
        print "========================================"
        bibcode = record.find('bibcode').text.encode('utf-8')

        print record.attrib
        print "title: " +  title
        print "bibcode: " + bibcode

        for author in record.iter('author'):
            print "\t" + author.text.encode('utf-8')

    # for record in root:
    #     print record.tag , record.attrib
    #     for author in record
    #         print record.find('author').text
    #     print record.find('bibcode').text
    #     print record.find('title').text


## download URL
def dowload_url (url, fileName):

    #print url
    ads_data = urllib2.urlopen(url)

    # Get the URL. This gets the real URL.
    #print "The URL is: ", ads_data.geturl()

    # Getting the code
    #print "This gets the code: ", ads_data.code

    # Get the Headers.
    # This returns a dictionary-like object that describes the page fetched,
    # particularly the headers sent by the server
    #print "The Headers are: ", ads_data.info()

    # Get the date part of the header
    #print "The Date is: ", ads_data.info()['date']

    # Get the server part of the header
    #print "The Server is: ", ads_data.info()['server']

    # Get all data
    print "Retrieving data from ADS..."
    html = ads_data.read()
    #print "Get all data: ", html

    # Get only the length
    #print "Get the length :", len(html)

    # Note that the rstrip strips the trailing newlines and carriage returns before
    # printing the output.

    # fileName to be written to




    #open the fileName for writing
    print "Writing file " + fileName
    fh = open(fileName, "w")

    # read from request while writing to fileName
    # Showing that the fileName object is iterable
    fh.write(html)



    # You can also use the with statement:
    #with open(fileName, 'w') as f: f.write(ads_data.read())
    fh.close()

    print "Finished"



##
##    start main program
##
url = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_url=YES&ned_url=YES&adsobj_url=YES&aut_logic=OR&obj_logic=OR&author=de+mink&object=&start_mon=&start_year=&end_mon=&end_year=&ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=1000&start_nr=1&jou_pick=ALL&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=CITATIONS&data_type=XML&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1"
fileName = "adw.xml"

#dowload_url (url, fileName)

#parse_xml("country_data.xml")
parse_xml(fileName)
