from django.apps import AppConfig

flag=False
idx=0
headlines=[]
toi_news=[]
ht_news=[]
toi_news_images=[]
ht_news_images=[]
all_data = []

class NewsConfig(AppConfig):
    name = 'news'
