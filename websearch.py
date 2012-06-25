from BeautifulSoup import BeautifulSoup
import mechanize
import cookielib
from fuzzywuzzy import fuzz

from search_result import SearchResult
from search_exception import SearchException

class WebSearch:
    def __init__(self,user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'):
        # Browser
        self.br = mechanize.Browser()

        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)    
        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)        
        self.br.set_handle_robots(False)
 
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), 
                              max_time=1)    
        self.br.addheaders =[('User-agent', user_agent)]

    def google(self, search_string):
        try:
            self.br.open('http://google.com')
        except:
            raise SearchException("Google: Internet failed or You're Blocked !!")

        try:
            self.br.select_form(nr=0)  
            self.br.form['q']= search_string 
        except Exception as e:
            print e
            raise SearchException("Google: page structure changed, API outsmarted") 

        try:
            self.br.submit()
            search_results_html = self.br.response().read()
        except:
            raise SearchException("Google: Response unreadable, ")

        results_soup = BeautifulSoup(
            search_results_html, convertEntities=BeautifulSoup.HTML_ENTITIES)

        result_summary=[]
        try:
            result_list = results_soup.findAll('li',{'class':'g'})

            for result in result_list:
                result_extract = SearchResult()
                result_extract.headline = result.find('a').text
                result_extract.link = result.find('a',href=True)['href']

                desc_block = result.find('span',{'class':'st'})
                if desc_block==None:
                    continue
                result_extract.description=desc_block.text
                result_extract.matched_phrases = [i.text for i in desc_block.findAll('em')]
                match_string = ' '.join(result_extract.matched_phrases)
                result_extract.matched_percent=fuzz.ratio(match_string.lower(),search_string.lower())
                #print match_string, search_string, result_extract.matched_percent
                result_summary.append(result_extract)
        except Exception as e:
            print e
            raise SearchException("Google: page structure changed, API outsmarted")
            
        return result_summary

    def yahoo(self, search_string):
        try:
            self.br.open('http://yahoo.com')
        except:
            raise SearchException("Yahoo: Internet failed or You're Blocked !!")

        try:
            self.br.select_form(nr=0)  
            self.br.form['p']= search_string 
        except Exception as e:
            print e
            raise SearchException("Yahoo: page structure changed, API outsmarted") 

        try:
            self.br.submit()
            search_results_html = self.br.response().read()
            #print search_results_html
        except:
            raise SearchException("Yahoo: Response unreadable, ")

        results_soup = BeautifulSoup(
            search_results_html, convertEntities=BeautifulSoup.HTML_ENTITIES)

        result_summary=[]
        try:
            result_list = results_soup.find('ol',{'start':'1'}).findAll('li')

            for result in result_list:
                result_extract = SearchResult()
                result_extract.headline = result.find('a').text
                try:
                    result_extract.link= "http://" + result.find('span',{'class':'url'}).text
                    desc_block = result.find('div',{'class':'abstr'})
                    result_extract.description=desc_block.text
                    result_extract.matched_phrases = [i.text for i in desc_block.findAll('b')]
                except:
                    continue

                if desc_block==None:
                    continue

                match_string = ' '.join(result_extract.matched_phrases)
                result_extract.matched_percent=fuzz.ratio(match_string.lower(),search_string.lower())
                #print match_string, search_string, result_extract.matched_percent
                result_summary.append(result_extract)
        except Exception as e:
            print e
            raise SearchException("Yahoo: page structure changed, API outsmarted")
            
        return result_summary
