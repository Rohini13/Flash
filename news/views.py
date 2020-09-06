from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# GEtting news from Times of India
toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BeautifulSoup(toi_r.content, 'html5lib')
toi_headings = toi_soup.find_all('h2')
toi_headings = toi_headings[0:25]
toi_news = []

for th in toi_headings:
    toi_news.append(th.text)


#Getting news from Hindustan times
#ht_r = requests.get("https://www.hindustantimes.com/india-news/")
ht_r = requests.get("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen")
ht_soup = BeautifulSoup(ht_r.content, 'html5lib')
ht_headings = ht_soup.findAll('h3')
ht_headings = ht_headings[0:25]
ht_news = []


for hth in ht_headings:
    ht_news.append(hth.text)


def index(req):
    print(len(ht_news))
    return render(req, 'news/index.html', {'toi_news':toi_news, 'ht_news': ht_news})