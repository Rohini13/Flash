import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sys import path
import os
path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from sources import NEWS_SOURCES
from helper import remove_duplicates


def get_all_dd_info(objects):

    def get_dd_info(obj):
        response = requests.get(obj["link"])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            contents = soup.find('div', {'class': 'news_content'})
            text = list()
            if contents:
                contents = contents.find_all('p', limit=2)
                text.append(contents[0].get_text())
                text.append(contents[1].get_text())
            obj["content"]=text
            title = soup.find("title")
            if title:
                obj['title'] = title.get_text()
            image_tag = soup.find("span", {"class": "field-content"})
            image = image_tag.find("img")
            if image:
                obj['image'] = image.get('src')
            list_class = ['social_share', 'detail_share']
            time_tag = soup.find("div", {"class" : list_class})
            time = time_tag.find("p", {"class" : "date"})
            if time:
                obj['time'] = time.get_text()

        return "NA"

    for obj in objects:
        if obj["link"] != "#":
            get_dd_info(obj)
        else:
            objects.remove(obj)


def get_dd_links(obj):
    if obj['href'][0] == '/':
        obj['href'] = 'http://ddnews.gov.in' + obj['href']
    try:
        return {
            "content": "NA",
            "link": obj["href"],
            "scraped_at": datetime.utcnow().isoformat(),
            "published_at": None,
            "title": "",
            "source": "DD News"
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_dd_articles(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        a_tags = list(
                    soup.find('div', {'class': 'view-content'}
                    ).find_all('a')
                )
        for a_tag in a_tags:
            if a_tag.get('target') == '_BLANK':
                a_tags.remove(a_tag)
        headlines = list(map(get_dd_links, a_tags))
        get_all_dd_info(headlines)  # Fetch contents separately
        return headlines
    return None