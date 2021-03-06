import urllib
import urllib2

from files import *
from xmllib import *
from Article import *
from Ranking import *

#constants
NAMESPACE = "{http://ads.harvard.edu/schema/abs/1.1/abstracts}"
XML_PATH = "./xml/" # check if directory exists
AUTHOR = 'de Mink, S. E.'

# global list of articles
author_articles = []
rankings = Rankings() #Rankings consist of an array of Ranking objects

def add_authors (record, article):
    """Loops through authors  of the record and adds them to the article """

    for item in record.iter(NAMESPACE + 'author'):
        tmpAuthor = item.text.encode('utf-8')
        article.add_author(tmpAuthor)

def parse_xml (fileName):
    """Parses the main XML with citations of the author"""

    print "Parsing XML: " + fileName
    tree = ET.parse(XML_PATH + fileName)
    root = tree.getroot()

    i=0
    for record in root:
        i=i+1
        curTitle= xml_value(record, NAMESPACE + 'title')

        curBibcode= xml_value(record, NAMESPACE + 'bibcode')
        print "Article " + str(i) + " :" +curBibcode
        curPubDate= xml_value(record, NAMESPACE + 'pubdate')

        citation_url =""
        for item in record.iter(NAMESPACE + 'link'):
            if item.attrib.get('type')=='CITATIONS':
                #print "citations found!"
                citation_url = xml_value(item, NAMESPACE + 'url')

        #citation_urls.append(citation_url)

        curArticle = Article(curBibcode, curTitle, citation_url)
        curArticle.pub_date = curPubDate
        add_authors (record, curArticle)

        if citation_url != "":
            #print "retrieveing citations for " + curBibcode
            citation_url = citation_url + "&data_type=XML"
            citationsFileName = curBibcode + ".xml"

            dowload_url(citation_url, citationsFileName)

            curArticle.num_citations = get_num_citations(citationsFileName)
        else:
            #print "no citations for " + curBibcode
            curArticle.num_citations = 0

        author_articles.append(curArticle)


def get_num_citations(fileName):
    """ Retrieves the number of citations from the citations XML"""
    #print "getting number of citations form XML: " + XML_PATH +  fileName
    tree = ET.parse(XML_PATH + fileName)
    root = tree.getroot()

    number_of_citations = root.attrib.get('retrieved')
    #print number_of_citations

    # print "retrieving authors in citation"
    # for record in root:
    #     print(xml_value(record, NAMESPACE + 'title'))
    #     xml_multiple_values(record, 'author')

    return int(number_of_citations)



def update_citations():
    """ Add citation-article to the main article-records """
    #print "updating citations"
    for article in author_articles: #loop door artikelen

        if article.num_citations>0:

            fileName = article.bibcode + ".xml"
            #print "getting citations form XML: " + fileName
            tree = ET.parse(XML_PATH + fileName)
            root = tree.getroot()

            # print "retrieving authors in citations"
            for record in root: #loop door citation artikelen
                tmpTitle = xml_value(record, NAMESPACE + 'title')
                tmpBibcode = xml_value(record, NAMESPACE + 'bibcode')
                citationArticle = Article (tmpBibcode, tmpTitle, "")

                authors = record.findall(NAMESPACE + 'author')
                for author in authors:
                    citationArticle.add_author(author.text.encode('utf-8'))

                article.add_citation(citationArticle)


def update_citation_count(authorToFind):
    """ updates the citation count of the article, excluding the main author """
    # print "updating citation counts for author" + authorToFind

    for article in author_articles: #loop door artikelen
        numCitations = article.num_citations
        if numCitations>0:
            #print numCitations
            for citation in article.citations: # loop door citaties van dit artikel
                for author in citation.authors: # loop door auteurs bij citaties van dit artikel
                    if author == authorToFind:
                        #print"self reference found"
                        numCitations = numCitations - 1
            #print numCitations
        article.num_citations_no_author = numCitations

def update_citation_count_all():
    """ updates the citation count, excluding all authors of the article """
    # print "updating citation counts for all authors"
    numCitations = 0
    found = False
    for article in author_articles: #loop door artikelen
        numCitations = 0
        for citation in article.citations: # loop door citaties van dit artikel
            found=False
            for cit_author in citation.authors: # loop door auteurs bij citaties van dit artikel
                for article_author in article.authors: #loop door auteurs van originele artikel
                    if cit_author == article_author:
                        #print"self reference found"
                        found=True

            if found == False:
                numCitations=numCitations + 1

        article.num_citations_no_all_authors = numCitations

def main_xml():
    print "Downloading articles for " + AUTHOR
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



    parameters['author'] = AUTHOR
    parameters['nr_to_return'] = 1000
    parameters['data_type'] = "XML"
    parameters['jou_pick'] = "ALL"
    parameters['sort'] = "SCORE"


    url = baseURL + "&" + urllib.urlencode(parameters)
    #print url

    fileName = "adw.xml"

    dowload_url (url, fileName)

    parse_xml(fileName)

def manage_citations():
    print "Manage citations"
    update_citations()
    update_citation_count(AUTHOR)
    update_citation_count_all()


def download_year(year):
    baseURL = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&obj_logic=OR&object=&ttl_logic=OR&title=&txt_logic=OR&text=&start_nr=1&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1"

    parameters = {
        "author" : "",
        "data_type" : "",
        "start_year" : "",
        "start_mon" :"",
        "end_mon": "",
        "end_year" : "",
        "nr_to_return" : "",
        "article_sel" : "",
        "jou_pick": "",
        "sort": "",
        "data_type:" : ""

    }


    parameters['start_year'] = year
    parameters['end_year'] = year
    parameters['nr_to_return'] = 1000
    parameters['article_sel'] = "YES"
    parameters['jou_pick'] = "NO"
    parameters['sort'] = "CITATIONS"
    parameters['data_type'] = "XML"

    print "downloading : " + str(year)
    url = baseURL + "&" + urllib.urlencode(parameters)
    #print url

    fileName = str(year) + ".xml"

    dowload_url (url, fileName)

def calculate_rankings(year):
    fileName = str(year) + ".xml"

    #print "Parsing XML: " + fileName
    tree = ET.parse(XML_PATH + fileName)
    root = tree.getroot()
    #print root.attrib

    #get selected attribute from root
    total_in_year = root.attrib.get('selected')
    ranking=0
    for record in root:
        ranking += 1
        curBibcode= xml_value(record, NAMESPACE + 'bibcode')
        #print "Adding: "  + str(ranking), str(year), total_in_year, curBibcode
        rankings.add(curBibcode, year, ranking, total_in_year)


def manage_ranking():
    print "Manage rankings"
    min_year = 999999;
    max_year = 0;
    for article in author_articles:
        tmpYear = article.getYear()
        if tmpYear > max_year:
            max_year =  tmpYear
        if tmpYear < min_year:
            min_year = tmpYear

    #print "Year range: ["  + str(min_year) + ", " + str(max_year) + "]"

    # download xml from ads website
    for year in range (min_year, max_year):
        download_year(year)

    # create rankings table
    for year in range (min_year, max_year):
        calculate_rankings(year)

    # update article with ranking
    # TODO: uses 2 loops which is not very efficient
    for article in author_articles:
        objRank = rankings.getRankingObj(article.bibcode)
        if objRank != None:
            article.ranking = objRank.ranking
            article.percentiel = objRank.percentiel
            article.total_in_year = objRank.total
    #rankings.show()

def save():
    fileName = XML_PATH + "article_export" + ".txt"
    print "Saving file to " + fileName
    fh = open(fileName, "w")

    for article in author_articles:
        fh.write ("Bibcode:                  %s\n" % article.bibcode)
        fh.write ("Title:                    %s\n" % article.title)
        fh.write ("Publication date:         %s\n" % article.pub_date)
        fh.write ("Citations:                %i\n" % article.num_citations)
        fh.write ("Citations (excl author):  %i\n" % article.num_citations_no_author)
        fh.write ("Citations (excl all):     %i\n" % article.num_citations_no_all_authors)
        fh.write ("Ranking in year:          %i\n" % article.ranking)
        fh.write ("Total in year:            %i\n" % article.total_in_year)
        fh.write ("Percentile in year:       %f\n" % article.percentiel)
        fh.write ("\n")
        fh.write ("---------------------------------\n")
        fh.write ("\n")

    fh.close()


## ------------------------
##    start main program
## ------------------------

# download main XML with abstracts from author
main_xml()

# Step 1: manage citation count
manage_citations()

# Step 2: manage rankings
manage_ranking()

save()

# print articles
# for article in author_articles:
#     article.show()
