import os
from sys import path
import requests
from bs4 import BeautifulSoup

path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from helper import (is_string, ist_to_utc, remove_duplicates,str_is_set)


def get_all_content(objects):
    """
    Call this function with a list of objects. Make sure there are no duplicate
    copies of an object else downloading might take long time.
    """
    def get_content(url):
        response = requests.get(url)
        if response.status_code == 200:
            html_content = BeautifulSoup(response.text, "html.parser")
            contents = html_content.find(
                        'div', {'class': 'story-details'}
                        )
            if not contents:
                return "NA"
            contents = contents.find_all('p')
            text = ''
            for cont in contents[:-1]:
                if cont.string:
                    text += cont.string + '\n'
            return text
        return "NA"

    for obj in objects:
        obj["content"] = get_content(obj["link"])


def get_headline_details(obj):
    try:
        from datetime import datetime
        timestamp_tag = obj.parent.parent.find(
            "span", {"class": "time-dt"}
        )
        if timestamp_tag is None:
            timestamp = datetime.now()
        else:
            content = timestamp_tag.contents[0].strip()
            timestamp = datetime.strptime(
                content,
                "%b %d, %Y %H:%M"
            )
        return {
            "content": "NA",
            "link": obj["href"].split("?")[0],
            "scraped_at": datetime.utcnow().isoformat(),
            "published_at": ist_to_utc(timestamp).isoformat(),
            "title": "\n".join(filter(
                str_is_set,
                map(
                    str.strip,
                    filter(is_string, obj.children)
                )
            ))
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_chronological_headlines(url):
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        a_tags = list(map(
            lambda x: x.find("a"),
            soup.find_all("div", {
                "class": "media-body"
            })
        ))
        headlines = remove_duplicates(list(map(get_headline_details, a_tags)), 'link')
        get_all_content(headlines)
        return headlines
    return None

