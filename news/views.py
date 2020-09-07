from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import pyttsx3
from . import apps

headlines=[]
# Getting news from Times of India
toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BeautifulSoup(toi_r.content, 'html5lib')
toi_headings = toi_soup.find_all('h2')
toi_headings = toi_headings[3:20]
toi_news = []

headlines.append('News from Times of India are as follows:')
for th in toi_headings:
    headlines.append(th.text)
    toi_news.append(th.text)

# Getting news from Hindustan Times
ht_r = requests.get("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen")
ht_soup = BeautifulSoup(ht_r.content, 'html5lib')
ht_headings = ht_soup.findAll('h3')
ht_headings = ht_headings[3:20]
ht_news = []

headlines.append('News from Hindustan Times are as follows:')
for hth in ht_headings:
    headlines.append(hth.text)
    ht_news.append(hth.text)


def index(req):
    return render(req, 'news/index.html', {'toi_news':toi_news, 'ht_news': ht_news})

def readAloud(req):
    engine = pyttsx3.init()
    end = len(headlines)
    start = apps.idx%end
    for i in range(start,end):
        if apps.flag:
            apps.idx=i%end
            break
        engine.say(headlines[i])
        engine.runAndWait()
    apps.flag=False
    return render(req, 'news/index.html', {'toi_news': toi_news, 'ht_news': ht_news})

def stop(req):
    apps.flag = True
    return redirect('/')