import urllib
import urllib2

from files import *
from xmllib import *
from Article import *

author_articles = []

def add_authors (record, article):

    for item in record.iter('author'):
        tmpAuthor = item.text.encode('utf-8')
        article.add_author(tmpAuthor)

## Parse XML
def parse_xml (fileName):

    print
    print "Parsing XML: " + fileName
    tree = ET.parse(xml_path + fileName)
    root = tree.getroot()


    #print root.tag
    #print root.attrib

    for record in root:
        # print
        curTitle= xml_value(record, 'title')
        curBibcode= xml_value(record, 'bibcode')
        citation_url =""
        #print record.attrib


        #xml_multiple_values(record, 'keyword')
        for item in record.iter('link'):
            #print item.attrib
            if item.attrib.get('type')=='CITATIONS':
                #print "citation found!"
                citation_url = xml_value(item, 'url')

        #citation_urls.append(citation_url)

        curArticle = Article(curBibcode, curTitle, citation_url)
        add_authors (record, curArticle)

        if citation_url != "":
            #print "retrieveing citations for " + curBibcode
            citation_url = citation_url + "&data_type=XML"
            citationsFileName = curBibcode + ".xml"
            # TODO: de volgende weer aan zetten als de citations weer gedownload
            # moeten worden
            #dowload_url(citation_url, citationsFileName)

            curArticle.num_citations = get_num_citations(citationsFileName)



        else:
            #print "no citations for " + curBibcode
            curArticle.num_citations = 0

        author_articles.append(curArticle)
##
## File functions
##

## download URL

##
## Abstract functions
##

def get_num_citations(fileName):
        #print "getting number of citations form XML: " + fileName
        tree = ET.parse(xml_path + fileName)
        root = tree.getroot()

        number_of_citations = root.attrib.get('retrieved')
        #print number_of_citations

        # print "retrieving authors in citation"
        # for record in root:
        #     print(xml_value(record, 'title'))
        #     xml_multiple_values(record, 'author')

        return int(number_of_citations)



def update_citations():
    #print "updating citations"
    for article in author_articles: #loop door artikelen

        if article.num_citations>0:

            fileName = article.bibcode + ".xml"
            #print "getting citations form XML: " + fileName
            tree = ET.parse(xml_path + fileName)
            root = tree.getroot()

            # print "retrieving authors in citations"
            for record in root: #loop door citation artikelen
                tmpTitle = xml_value(record, namespace + 'title')
                tmpBibcode = xml_value(record, namespace + 'bibcode')
                citationArticle = Article (tmpBibcode, tmpTitle, "")

                authors = record.findall(namespace + 'author')
                for author in authors:
                    citationArticle.add_author(author.text.encode('utf-8'))

                article.add_citation(citationArticle)


def update_citation_count(authorToFind):
    print "updating citation counts for author" + authorToFind

    for article in author_articles: #loop door artikelen
        numCitations = article.num_citations
        if numCitations>0:
            #print numCitations
            for citation in article.citations: # loop door citaties van dit artikel
                for author in citation.authors: # loop door auteurs bij citaties van dit artikel
                    if author == authorToFind:
                        #print"self reference found"
                        numCitations = numCitations - 1
            #update citations
            #print numCitations
        article.num_citations_no_author = numCitations

def update_citation_count_all():
    print "TODO: Fix: updating citation counts for all authors"

    for article in author_articles: #loop door artikelen
        found = False
        numCitations = article.num_citations
        #print numCitations
        for article_authors in article.authors: # loop door auteurs bij artikelen
            for citation in article.citations: # loop door citaties van dit artikel
                for author in citation.authors: # loop door auteurs bij citaties van dit artikel
                    if author == article_authors:
                        #print"self reference found"
                        found=True
            if found==True:
                numCitations=numCitations - 1
        article.num_citations_no_all_authors = numCitations


##
##    start main program
##

# Split base url form paramaters
# parameters can be changed according to the step in the proces
baseURL = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&obj_logic=OR&object=&start_mon=&ttl_logic=OR&title=&txt_logic=OR&text=&start_nr=1&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1"

parameters = {
    "author" : "",
    "data_type" : "",
    "start_year" : "",
    "end_year" : "",
    "nr_to_return" : "",
    "query_type" : "",
    "article_sel" : "",
    "jou_pick": "",
    "sort": ""
}



parameters['author'] = "de+mink"
parameters['nr_to_return'] = 1000
parameters['data_type'] = "XML"
parameters['jou_pick'] = "ALL"
parameters['sort'] = "SCORE"
#parameters['start_year'] =2012
#parameters['end_year'] =2012
#parameters['query_type'] = "CITES"

url = baseURL + "&" + urllib.urlencode(parameters)
#print url

fileName = "adw.xml"


#dowload_url (url, fileName)

parse_xml(fileName)
print"--------------------------"
update_citations()
update_citation_count('de Mink, S. E.')
update_citation_count_all()

for article in author_articles:
    article.show()

#voor 2e ronde
# article_sel=YES
# jou_pick=NO #ALL
# sort=CITATIONS # SCORE
