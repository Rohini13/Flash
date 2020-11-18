import os
from sys import path
from datetime import datetime
import requests
from bs4 import BeautifulSoup

path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from helper import remove_duplicates
from sources import NEWS_SOURCES


def get_all_ndtv_info(objects):

    def get_ndtv_info(obj):
        response = requests.get(obj["link"])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find('title')
            if title:
                obj['title'] = title.get_text()
            classList = ['sp-cn', 'ins_storybody']
            contents = soup.find('div', {'class': classList})
            text = list()
            if contents:
                location_tag = contents.find('b')
                if location_tag:
                    obj['location'] = location_tag.get_text()
                contents_text = contents.find_all('p', limit=5)
                for i in range(len(contents_text)):
                    if i != 0:
                        if contents_text[i].get_text() != "":
                            text.append(contents_text[i].get_text())
                image = contents.find('img')
                if image:
                    obj['image'] = image.get('data-src')
                else:
                    obj['image'] = "https://cdn.ndtv.com/common/images/ogndtv.png"
            else:
                obj['image'] = "https://cdn.ndtv.com/common/images/ogndtv.png"
            obj["content"] = text
            time_tag = soup.find("span", {"itemprop" : "dateModified"})
            if time_tag:
                obj['time'] = time_tag.get_text()

    for obj in objects:
        get_ndtv_info(obj)


def get_ndtv_links(obj):
    if obj['href'][0] == '/':
        obj['href'] = 'https://www.ndtv.com/' + obj['href']
    try:
        return {
            "content": "NA",
            "link": obj["href"].split("?")[0],
            "scraped_at": datetime.utcnow().isoformat(),
            "published_at": None,
            "title": "",
            "source": "The NDTV News",
            "logo": "news/images/ndtv.png"
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_ndtv_articles(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        a_tags = list(map(
            lambda x: x.find("a"),
            soup.find_all("div", {
                "class": "new_storylising_img"
            }, limit=20)
        ))
        #a_tags = a_tags[0:17]
        headlines = list(map(get_ndtv_links, a_tags))
        headlines = remove_duplicates(headlines, "link")
        get_all_ndtv_info(headlines)  # Fetch contents separately
        return headlines
    return None
