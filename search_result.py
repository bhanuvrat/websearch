class SearchResult:
    def __init__(self):
        self.headline=''
        self.link=''
        self.description=''
        self.matched_phrases=[]
        self.matched_percent=0
    def __str__(self):
        print self.description
        return repr(self.headline) + repr(self.matched_phrases) + repr(self.link) + repr(self.matched_percent)
