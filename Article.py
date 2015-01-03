class Article:
    """ Article class
    Uses reference to array of citations of type Article """
    def __init__(self, bibcode, title, citation_url):
        self.bibcode = bibcode
        self.title = title
        self.citation_url = citation_url
        self.authors = []
        self.citations = [] # article
        self.num_citations = 0
        self.num_citations_no_author =0
        self.num_citations_no_all_authors = 0
        self.pub_date = ""
        self.ranking = 0
        self.total_in_year = 0
        self.percentiel = 0.0

    def add_author(self, author_name):
        self.authors.append (author_name)

    def add_citation (self, citation):
        self.citations.append(citation)

    def show(self):
        print "bibcode:                  " + self.bibcode
        print "title:                    " + self.title
        print "Publication date:         " + self.pub_date
        print "Year:                     " + str(self.getYear())
        # print "citation URL:             " + self.citation_url
        print "authors:"
        print self.authors
        # for author in self.authors:
        #     print "\t" + author
        print "#citations:               " + str(self.num_citations)
        print "#citations (excl author): " + str(self.num_citations_no_author)
        print "#citations (excl all):    " + str(self.num_citations_no_all_authors)
        print "ranking in year:          " + str(self.ranking)
        print "total in year:            " + str(self.total_in_year)
        print "percentiel in year:       " + str(self.percentiel)
        # print "#citation objects:        " + str(len(self.citations))
        # i = 1
        # for curCitation in self.citations:
        #     print "citation " + str(i) + ": "
        #     curCitation.showSimple()
        #     i = i + 1
        print "---------------------------------"

    def showSimple(self):
        print "\tbibcode:                  " + str(self.bibcode)
        #print "title:                    " + str(self.title)
        print "\tauthors:"
        print self.authors
        print "\t---------------------------------"

    def getYear(self):
        return int(self.pub_date[-4:])
