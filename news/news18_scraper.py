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
            # for tag in soup.find_all("div",{ "class":"Article_hideDiv__1quCc"}):
            #     print(tag)
            #     for t in tag.find_all("strong", {"id":"location_info" }):
            #         obj['location'] = t.get_text()
            if soup.find("ul",{"class":"Article_tags_bnow__3SqSZ"}) is not None:
                obj['time']=soup.find("ul",{"class":"Article_tags_bnow__3SqSZ"}).find_all('li')[1].get_text()[17:-3]
            text = list()
            print(obj['time'])
            for tag in soup.find_all("article", {"class":"Article_article_content_box__2nGyy"}):
                for t in tag.find_all("p", limit=10):
                    text.append(t.get_text())
            obj["content"] = text
            for tag in soup.find_all("div", {"class": "Article_article_box__3UQg5"}):
                obj['title']=tag.find("h1").get_text()
            for tag in soup.find_all("div", {"class": "Article_article_bimg__2Wo2a"}):
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
        if soup.find("div", {"class": "blog-list-blog"}) is None:
            return None
        a_list = soup.find_all("div", {"class": "blog-list-blog"}, limit=20)
        a_tags = list()
        for listele in a_list:
            if listele.find("a") is not None:
                a_tags.append(listele.find("a"))
        # a_tags = (
        #         soup.find("div", {"class": "blog-list-blog"}).find_all("a", limit=20)
        # )
        print(len(a_tags))
        headlines = remove_duplicates(map(get_links, a_tags),"link")
        get_all_info(headlines)
        return headlines
    return None
