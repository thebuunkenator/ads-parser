class Ranking:
    """ Ranking class """

    def __init__(self, bibcode, year, ranking, total):
        self.bibcode = bibcode  # string
        self.year = year        # int
        self.ranking = ranking  # int
        self.total = total      # int
        self.percentiel = 100.0*float(ranking)/float(total)


class Rankings:

    def __init__(self):
        self.rankings = []

    def add (self, bibcode, year, ranking, total):
        tmpRanking = Ranking(bibcode, int(year), int(ranking), int(total))
        self.rankings.append(tmpRanking)

    def getRankingObj(self, bibcode):
        tmpRank = None
        for rank in self.rankings:
            if bibcode == rank.bibcode:
                tmpRank = rank
                break
        return tmpRank

    def getRanking(self, bibcode): #returns int
        tmpRanking = 0
        for rank in self.rankings:
            if bibcode == rank.bibcode:
                tmpRanking = rank.ranking
                break
        return tmpRanking

    def getPercentiel(self, bibcode): # returns float
        tmpPercentiel = 0.0
        for rank in self.rankings:
            if bibcode == rank.bibcode:
                tmpPercentiel = 100.0*float(rank.ranking)/float(rank.total)
                break
        return tmpPercentiel

    def show(self):
        for rank in self.rankings:
            print rank.year, rank.ranking, rank.total, rank.percentiel, rank.bibcode
