class Article:

    def __init__(self, bibcode, title, citation_url):
        self.bibcode = bibcode
        self.title = title
        self.citation_url = citation_url
        self.authors = []
        self.citations = [] # article
        self.num_citations = 0
        self.num_citations_no_author =0
        self.num_citations_no_all_authors = 0

    def add_author(self, author_name):
        self.authors.append (author_name)

    def add_citation (self, citation):
        self.citations.append(citation)

    def show(self):
        print "bibcode:                  " + self.bibcode
        print "title:                    " + self.title
        print "citation URL:             " + self.citation_url
        print "authors:"
        for author in self.authors:
            print "\t" + author
        print "#citations:               " + str(self.num_citations)
        print "#citations (excl author): " + str(self.num_citations_no_author)
        print "#citations (excl all):    " + str(self.num_citations_no_all_authors)
        # for cite in citations:
            # print cite.title
        print "#citation objects:        " + str(len(self.citations))
        print "---------------------------------"


#toekomstige parameters

    #xml_value(record, 'affiliation')
    #xml_value(record, 'journal')
    #xml_value(record, 'volume')
    #xml_value(record, 'pubdate')
    #xml_value(record, 'page')
    #xml_value(record, 'url')
    #xml_value(record, 'score')
    #xml_value(record, 'citations')
