from datetime import datetime
from sys import path
import os
import requests
from bs4 import BeautifulSoup
path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from helper import ist_to_utc


def get_articles(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        soup.find("div",id="c_articlelist_widgets_1").decompose()
        data = []
        temp = soup.find("div",{"class":"main-content"})
        objs = temp.find_all("div", {"class":"top-newslist"})
        for obj in objs[0].find("ul"):
            data.append({
                    "link": "https://timesofindia.indiatimes.com"+obj.find("a").get("href"),
                    "content": "NA",
                    "scraped_at": datetime.utcnow().isoformat(),
                    "source" : "Times of India",
                    "location": None,
                    "time": None,
                    "title": obj.find("a").get("title")
                })
        return data