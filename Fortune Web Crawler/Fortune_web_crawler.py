from bs4 import BeautifulSoup 
import urllib 
import requests
import re
import numpy as np

class FORTUNE_web_crawler:
    
    def __init__(self, term, page_num):
            self.term = term 
            self.page_num = page_num
            self.url = 'http://fortune.com/search/?q={0}'.format(self.term)
            self.url_new = self.url + '&page={0}'.format(self.page_num)

    def run_web_crawler(self):
            req = urllib.request.Request(self.url_new)
            response = urllib.request.urlopen(req)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            result = soup.findAll('a', attrs={'href': re.compile("^http://fortune.com")}) 
            l = len(result)
            result = result[40:(l-35)]
            l_new = len(result)
            result_new = [result[2*i+1] for i in range(int(l_new/2))]
            result_new = result_new[1:len(result)]
            links = []
            for j in range(len(result_new)):
                links.append(result_new[j].get('href'))
            news_titles = []
            news_articles = []
            for k in range(len(result_new)):
                req_news = urllib.request.Request(links[k])
                response_news = urllib.request.urlopen(req_news)
                html_news = response_news.read()
                soup_news = BeautifulSoup(html_news,'html.parser')
                news_titles.append(soup_news.title)
                news_articles.append(soup_news.findAll('p'))
            news_titles_links = []
            for l in range(len(result_new)):
                news_titles_links.append([news_titles[l], news_articles[l], links[l]])
            return(news_titles_links)



article_titles_links = []
	
for i in range(3):
    crawler = FORTUNE_web_crawler(term = 'AI', page_num = str(i+1))
    outcome = crawler.run_web_crawler()
    article_titles_links = article_titles_links + outcome

news_data = []
for i in range(len(article_titles_links)):
     news_data.append(article_titles_links[i][0:3])


import csv
with open('news_data.csv', 'w') as myfile:
    wr = csv.writer(myfile, delimiter=',', lineterminator='\n')
    wr.writerow(['title', 'article', 'link'])
    for item in news_data:
        wr.writerow([item[0], item[1], item[2]])


# with open(file_path, 'a') as outcsv:   
#    #configure writer to write standard csv file
#    writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
#    writer.writerow(['number', 'text', 'number'])
#    for item in list:
#        #Write item to outcsv
#        writer.writerow([item[0], item[1], item[2]])
                
            
