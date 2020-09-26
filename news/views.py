from django.shortcuts import render, redirect
import os
from sys import path
import requests
from bs4 import BeautifulSoup
import pyttsx3
from . import apps
from django.contrib import auth
import pyrebase
from datetime import datetime, timezone, timedelta

path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import news18_scraper as n18S
import toi_scraper as toiS
from sources import NEWS_SOURCES

config = {
    'apiKey': "AIzaSyA7HJuzOo0HtJHZ7JZzv5yRszv7NjXNdps",
    'authDomain': "flash-94511.firebaseapp.com",
    'databaseURL': "https://flash-94511.firebaseio.com",
    'projectId': "flash-94511",
    'storageBucket': "flash-94511.appspot.com",
    'messagingSenderId': "72525595158",
    'appId': "1:72525595158:web:e642b67374c69b05f02b37",
    'measurementId': "G-5NQB6CC1JK"
}
firebase = pyrebase.initialize_app(config)
authenticate = firebase.auth()
database = firebase.database()


def signIn(request):
    return render(request, "news/signin.html")


def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authenticate.sign_in_with_email_and_password(email, password)
    except:
        message = "Invalid Credentials"
        return render(request, "news/signin.html", {"msg": message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    return render(request, "news/welcome.html", {"e": email})


def logout(request):
    auth.logout(request)
    return render(request, "news/signin.html")


def signUp(request):
    return render(request, "news/signup.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate.create_user_with_email_and_password(email, password)
    uid = user['localId']
    data = {"name": name, "status": "1"}
    database.child("users").child(uid).child("details").set(data)

    return render(request, "news/signin.html")


def index(req):
    toiURL = NEWS_SOURCES["Times of India"]["home"]
    news18URL = NEWS_SOURCES["NEWS18"]["home"]
    title = "Recent Headlines"
    return display(req, toiURL, news18URL, title)


def index1(req):
    toiURL = NEWS_SOURCES["Times of India"]["world"]
    news18URL = NEWS_SOURCES["NEWS18"]["world"]
    title = "World"
    return display(req, toiURL, news18URL, title)


def index2(req):
    toiURL = NEWS_SOURCES["Times of India"]["local"]
    news18URL = NEWS_SOURCES["NEWS18"]["local"]
    title = "Local"
    return display(req, toiURL, news18URL, title)


def index3(req):
    toiURL = NEWS_SOURCES["Times of India"]["technology"]
    news18URL = NEWS_SOURCES["NEWS18"]["technology"]
    title = "Science and Technology"
    return display(req, toiURL, news18URL, title)


def index4(req):
    toiURL = NEWS_SOURCES["Times of India"]["business"]
    news18URL = NEWS_SOURCES["NEWS18"]["business"]
    title = "Business and Economy"
    return display(req, toiURL, news18URL, title)


def index5(req):
    toiURL = NEWS_SOURCES["Times of India"]["health"]
    news18URL = NEWS_SOURCES["NEWS18"]["health"]
    title = "Health and Lifestyle"
    return display(req, toiURL, news18URL, title)


def index6(req):
    toiURL = NEWS_SOURCES["Times of India"]["sports"]
    news18URL = NEWS_SOURCES["NEWS18"]["sports"]
    title = "Sports"
    return display(req, toiURL, news18URL, title)


def index7(req):
    toiURL = NEWS_SOURCES["Times of India"]["entertainment"]
    news18URL = NEWS_SOURCES["NEWS18"]["entertainment"]
    title = "Entertainment"
    return display(req, toiURL, news18URL, title)


def display(req, toiURL, news18URL, title):
    # apps.idx = 0
    # apps.headlines = []
    # toi_r = requests.get(toiURL)
    # toi_soup = BeautifulSoup(toi_r.content, 'html5lib')
    # toi_headings = toi_soup.find_all('h2')
    # toi_images = toi_soup.find_all('img')
    # toi_headings = toi_headings[2:20]
    # toi_images = toi_images[3:20]
    # apps.toi_news = []
    # apps.toi_news_images = []
    # apps.ht_news_images = []
    #
    # apps.headlines.append('News from Times of India are as follows:')
    # for th in toi_headings:
    #     apps.headlines.append(th.text)
    #     apps.toi_news.append(th.text)
    #
    # for ti in toi_images:
    #     if 'data-src' in ti.attrs:
    #         apps.toi_news_images.append(ti.attrs['data-src'])

    toi_news = toiS.get_articles(toiURL.format(2))
    print(type(toi_news))
    n18_news = n18S.get_articles(news18URL.format(1))
    print(type(n18_news))

    return render(req, 'news/index.html',{'title':title, 'toi':toi_news, 'n18': n18_news})


def readAloud(req):
    engine = pyttsx3.init()
    end = len(apps.headlines)
    start = apps.idx % end
    for i in range(start, end):
        if apps.flag:
            apps.idx = i % end
            break
        engine.say(apps.headlines[i])
        engine.runAndWait()
    apps.flag = False
    return render(req, 'news/index.html',
    {'title': "Reading aloud...", 'toi_news': apps.toi_news, 'ht_news': apps.ht_news})


def stop(req):
    apps.flag = True
    return redirect('/')
