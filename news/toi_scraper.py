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
        #for tag in soup.find_all("div", {"id":"content"}):
         #   for t in tag.find_all("div", {"class":"wrapper clearfix politics"}):
          #      for b in t.find_all("div", {"class":"briefs_outer clearfix"}):
           #         objs = b.find_all("div", {"class":"brief_box"})
        objs = list()
        obj_tags = soup.find('div', {'class': "briefs_outer clearfix"})
        #print(obj_tags)
        if obj_tags:
            objs = obj_tags.find_all("div", {"class":"brief_box"}, limit=20)
        #print(objs)
        data = []
        # for tag in .find().find_all("div",{"class":"briefs_outer clearfix"}):
        #     objs = tag.find_all("div",{"class":"brief_box"})
        #     print(objs)
        for obj in objs:
            if(obj.find('a')!=None and obj.find('img')!=None):
                l="https://timesofindia.indiatimes.com"+obj.find('a').get('href')
                i=obj.find('img')
                c=obj.find("p").text
            else:
                continue
            text = list()
            text.append(c)
            data.append({
                    "link": l,
                    "content": text,
                    "scraped_at": datetime.now(),
                    "source" : "Times Of India",
                    "location": None,
                    "time": None,
                    "title": i.get("alt"),
                    "image": i.get("data-src"),
                    "logo":"news/images/toi.jpg"
                })
        return data