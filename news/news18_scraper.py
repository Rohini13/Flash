import os
from datetime import datetime
from sys import path

import requests
from bs4 import BeautifulSoup, NavigableString

path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from helper import remove_duplicates


def get_all_info(objects):

    def get_info(obj):
        response = requests.get(obj["link"])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup.find_all("div",{ "class":"article-bnow-box"}):
                for t in tag.find_all("strong", {"id":"location_info" }):
                    obj['location'] = t.get_text()
                if(tag.find("ul",{ "class":"article-bnow"})!=None):
                    obj['time']=tag.find("ul",{ "class":"article-bnow"}).find_all('li')[1].get_text()[14:-3]
            text = list()
            for tag in soup.find_all("article", {"class":"article-content-box first_big_character"}):
                for t in tag.find_all("p"):
                    text.append(t.get_text())
            obj["content"] = text
            for tag in soup.find_all("div", {"class": "article-box"}):
                obj['title']=tag.find("h1").get_text()
            for tag in soup.find_all("div", {"class": "article-bimg"}):
                obj['image']=tag.find("img").get('src')

    for obj in objects:
        get_info(obj)


def get_links(obj):
    if (obj['href'][0] == '/'):
        obj['href'] = 'https://www.news18.com' + obj['href']
    try:
        return {
            "content": "",
            "link": obj["href"].split("?")[0],
            "scraped_at": datetime.utcnow().isoformat(),
            "time": None,
            "location": None,
            "source": "CNN-News18",
            "title": "",
            "image": None,
            "logo": "news/images/news18.jpg"
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_articles(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        #for tag in soup.find_all("a", {"class": "vodeoiconb"}):
            #tag.parent.decompose()
        #for tag in soup.find_all("span", {"class": "video_icon_ss"}):
            #tag.parent.parent.decompose()
        if soup.find("div", {"class": "hotTopic"}) is None or soup.find("div", {"class": "blog-list"}) is None:
            return None
        a_tags = (
                soup.find("div", {"class": "hotTopic"}).find_all("a", limit=5) +
                soup.find("div", {"class": "blog-list"}).find_all("a", limit=5)
        )
        headlines = remove_duplicates(map(get_links, a_tags),"link")
        get_all_info(headlines)
        return headlines
    return None