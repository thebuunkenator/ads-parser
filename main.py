import urllib
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

    # Get all data
    print "Retrieving data from ADS..."
    html = ads_data.read()

    #open the fileName for writing
    print "Writing file " + fileName
    fh = open(fileName, "w")

    fh.write(html)

    fh.close()

    print "Finished"

##
##    start main program
##

# Split base url form paramaters
# parameters can be changed according to the step in the proces
baseURL = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&obj_logic=OR&object=&start_mon=&ttl_logic=OR&title=&txt_logic=OR&text=&start_nr=1&jou_pick=ALL&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=SCORE&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1"

parameters = {
"author" : "de+mink",
"data_type" : "XML", #possible values:
"start_year" : "",
"end_year" : "",
"nr_to_return" : "1000"
}


url = baseURL + "&" + urllib.urlencode(parameters)
fileName = "adw.xml"


#dowload_url (url, fileName)

#parse_xml("country_data.xml")
parse_xml(fileName)
