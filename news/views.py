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

from news18_scraper import get_articles
from dd_news import get_dd_articles
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
    urlVar = "https://timesofindia.indiatimes.com/briefs"
    news18URL = NEWS_SOURCES["NEWS18"]["home"]
    ddnewsURL = NEWS_SOURCES["DD News"]["home"]
    title = "Recent Headlines"
    return display(req, urlVar, news18URL, ddnewsURL, title)


def index1(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/world"
    news18URL = NEWS_SOURCES["NEWS18"]["world"]
    ddnewsURL = NEWS_SOURCES["DD News"]["world"]
    title = "World"
    return display(req, urlVar, news18URL, ddnewsURL, title)


def index2(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/india"
    news18URL = NEWS_SOURCES["NEWS18"]["local"]
    ddnewsURL = NEWS_SOURCES["DD News"]["local"]
    title = "Local"
    return display(req, urlVar, news18URL, ddnewsURL, title)


def index3(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/gadgets"
    news18URL = NEWS_SOURCES["NEWS18"]["technology"]
    ddnewsURL = NEWS_SOURCES["DD News"]["technology"]
    title = "Science and Technology"
    return display(req, urlVar, news18URL, ddnewsURL, title)


def index4(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/business"
    news18URL = NEWS_SOURCES["NEWS18"]["business"]
    ddnewsURL = NEWS_SOURCES["DD News"]["business"]
    title = "Business and Economy"
    return display(req, urlVar, news18URL, ddnewsURL, title)


def index5(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/lifestyle"
    news18URL = NEWS_SOURCES["NEWS18"]["health"]
    ddnewsURL = NEWS_SOURCES["DD News"]["health"]
    title = "Health and Lifestyle"
    return display(req, urlVar, news18URL, ddnewsURL, title)


def index6(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/sports"
    news18URL = NEWS_SOURCES["NEWS18"]["sports"]
    ddnewsURL = NEWS_SOURCES["DD News"]["sports"]
    title = "Sports"
    return display(req, urlVar, news18URL, ddnewsURL, title)


def index7(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/entertainment"
    news18URL = NEWS_SOURCES["NEWS18"]["entertainment"]
    ddnewsURL = NEWS_SOURCES["DD News"]["entertainment"]
    title = "Entertainment"
    return display(req, urlVar, news18URL, ddnewsURL, title)


def display(req, urlVar, news18URL, ddnewsURL, title):
    apps.idx = 0
    apps.headlines = []
    toi_r = requests.get(urlVar)
    toi_soup = BeautifulSoup(toi_r.content, 'html5lib')
    toi_headings = toi_soup.find_all('h2')
    toi_images = toi_soup.find_all('img')
    toi_headings = toi_headings[2:20]
    toi_images = toi_images[3:20]
    apps.toi_news = []
    apps.toi_news_images = []
    apps.ht_news_images = []

    apps.headlines.append('News from Times of India are as follows:')
    for th in toi_headings:
        apps.headlines.append(th.text)
        apps.toi_news.append(th.text)

    for ti in toi_images:
        if 'data-src' in ti.attrs:
            apps.toi_news_images.append(ti.attrs['data-src'])

    n18_news = get_articles(news18URL.format(1))
    dd_news = get_dd_articles(ddnewsURL.format(1))
    for dd in dd_news:
        if dd["link"] == "#":
            dd_news.remove(dd)
        if dd["content"] == "":
            dd_news.remove(dd)
    print(dd_news)

    return render(req, 'news/index.html',{'title':title, 'range1': range(len(apps.toi_news_images)), 'toi_news': apps.toi_news,'toi_news_images': apps.toi_news_images, 'n18': n18_news, 'dd': dd_news})


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
