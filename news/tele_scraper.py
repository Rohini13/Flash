import os
from sys import path
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from helper import (is_string, ist_to_utc, remove_duplicates,str_is_set)


def get_all_info(objects):
    def get_info(obj):
        url=obj['link']
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup.find_all("div",{ "class":"container uk-background-default pt-2"}):
                for t in tag.find_all("div",{ "class":"row uk-grid-divider pt-2"}):
                    for q in t.find_all("div",{ "class":"col-8"}):
                        for r in q.find_all("div", {"row uk-grid-divider"}):
                            for s in r.find_all("div", {"class": "col-12"}):
                                for u in s.find_all("div", {"class": "article pb-4"}):
                                    obj['title']=u.find_all("div")[1].find("h1").text.strip()
                                    obj['image']=u.find_all("div")[3].find("img").get('src')
                                    obj['location'] = u.find_all("div")[7].find("div").find_all("span")[1].get_text()
                                    obj['time'] = u.find_all("div")[7].find("div").find_all("span")[2].get_text()
                                    for c in u.find_all("div")[9].find_all("p"):
                                        obj['content'] = obj['content'] + ' '+c.get_text()


        return "NA"

    for obj in objects:
        get_info(obj)
        # print(obj)


def get_links(obj):
    obj = 'https://www.telegraphindia.com' + obj
    try:
        return {
            "content": "",
            "link": obj,
            "scraped_at": datetime.utcnow().isoformat(),
            "time": None,
            "location": None,
            "source": "The Telegraph",
            "title": "",
            "image": None
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_articles(url):
    response = requests.get(url)
    print(response.status_code)
    a_tags=[]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for tags in soup.find_all("div", {"class": "container uk-background-default pt-3 mainContainer"}):
            for t in tags.find_all("div", {"class": "row uk-grid-divider pb-3"}):
                for b in t.find_all("div", {"class": "col-8"}):
                    # print(b)
                    for a in b.find_all("div", {"class":"row pb-3 pt-3"}):
                        # print(a)
                        for c in a .find_all("div", {"class":"col-5"}):
                            # print(c)
                            for d in c.find_all("div",{"class":"asp_16_9"}):
                                # print(d)
                                a_tags.append(d.find("a").get('href'))

        # print(a_tags)
        headlines = list(map(get_links, a_tags))
        get_all_info(headlines)
        return headlines
    return None