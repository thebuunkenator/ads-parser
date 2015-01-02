import urllib
import urllib2
import os
import xml.etree.ElementTree as ET

def xml_value (record, parameter):
    if record.find(parameter) != None:
        value = record.find(parameter).text.encode('utf-8')
        print parameter + ": "  + value
    else:
        print parameter + ": not found."

def xml_multiple_values (record, parameter):
    print parameter + 's:'
    for item in record.iter(parameter):
        print "\t" + item.text.encode('utf-8')

## Parse XML
def parse_xml (fileName):

    print
    print "Parsing XML: " + fileName
    tree = ET.parse(fileName)
    root = tree.getroot()


    print root.tag
    print root.attrib

    for record in root:

        print
        print "--------------------------------------------------------------------------"
        xml_value(record, 'title')
        print "--------------------------------------------------------------------------"
        xml_value(record, 'bibcode')

        #print record.attrib

        xml_value(record, 'affiliation')
        xml_value(record, 'journal')
        xml_value(record, 'volume')
        xml_value(record, 'pubdate')
        xml_value(record, 'page')
        xml_value(record, 'url')
        xml_value(record, 'score')
        xml_value(record, 'citations')

        xml_multiple_values(record, 'author')
        xml_multiple_values(record, 'keyword')


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
"author" : "",
"data_type" : "",
"start_year" : "",
"end_year" : "",
"nr_to_return" : "",
"query_type" : ""
}

parameters['author'] = "de+mink"
parameters['nr_to_return'] = 1000
parameters['data_type'] = "XML"
#parameters['start_year'] =2012
#parameters['end_year'] =2012
#parameters['query_type'] = "CITES"

url = baseURL + "&" + urllib.urlencode(parameters)
#print url

fileName = "adw.xml"


#dowload_url (url, fileName)

#parse_xml("country_data.xml")
parse_xml(fileName)
