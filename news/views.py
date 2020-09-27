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
from dd_news_scraper import get_dd_articles
from ndtv_scraper import get_ndtv_articles
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
    ddnewsURL = NEWS_SOURCES["DD News"]["home"]
    ndtvURL = NEWS_SOURCES["NDTV"]["home"]
    title = "Recent Headlines"
    return display(req, toiURL, news18URL, ddnewsURL, ndtvURL, title)


def index1(req):
    toiURL = NEWS_SOURCES["Times of India"]["world"]
    news18URL = NEWS_SOURCES["NEWS18"]["world"]
    ddnewsURL = NEWS_SOURCES["DD News"]["world"]
    ndtvURL = NEWS_SOURCES["NDTV"]["world"]
    title = "World"
    return display(req, toiURL, news18URL, ddnewsURL, ndtvURL, title)


def index2(req):
    toiURL = NEWS_SOURCES["Times of India"]["local"]
    news18URL = NEWS_SOURCES["NEWS18"]["local"]
    ddnewsURL = NEWS_SOURCES["DD News"]["local"]
    ndtvURL = NEWS_SOURCES["NDTV"]["local"]
    title = "Local"
    return display(req, toiURL, news18URL, ddnewsURL, ndtvURL, title)


def index3(req):
    toiURL = NEWS_SOURCES["Times of India"]["technology"]
    news18URL = NEWS_SOURCES["NEWS18"]["technology"]
    ddnewsURL = NEWS_SOURCES["DD News"]["technology"]
    ndtvURL = NEWS_SOURCES["NDTV"]["technology"]
    title = "Science and Technology"
    return display(req, toiURL, news18URL, ddnewsURL, ndtvURL, title)

def index4(req):
    toiURL = NEWS_SOURCES["Times of India"]["business"]
    news18URL = NEWS_SOURCES["NEWS18"]["business"]
    ddnewsURL = NEWS_SOURCES["DD News"]["business"]
    ndtvURL = NEWS_SOURCES["NDTV"]["business"]
    title = "Business and Economy"
    return display(req, toiURL, news18URL, ddnewsURL, ndtvURL, title)


def index5(req):
    toiURL = NEWS_SOURCES["Times of India"]["health"]
    news18URL = NEWS_SOURCES["NEWS18"]["health"]
    ddnewsURL = NEWS_SOURCES["DD News"]["health"]
    ndtvURL = NEWS_SOURCES["NDTV"]["health"]
    title = "Health and Lifestyle"
    return display(req, toiURL, news18URL, ddnewsURL, ndtvURL, title)


def index6(req):
    toiURL = NEWS_SOURCES["Times of India"]["sports"]
    news18URL = NEWS_SOURCES["NEWS18"]["sports"]
    ddnewsURL = NEWS_SOURCES["DD News"]["sports"]
    ndtvURL = NEWS_SOURCES["NDTV"]["sports"]
    title = "Sports"
    return display(req, toiURL, news18URL, ddnewsURL, ndtvURL, title)


def index7(req):
    toiURL = NEWS_SOURCES["Times of India"]["entertainment"]
    news18URL = NEWS_SOURCES["NEWS18"]["entertainment"]
    ddnewsURL = NEWS_SOURCES["DD News"]["entertainment"]
    ndtvURL = NEWS_SOURCES["NDTV"]["entertainment"]
    title = "Entertainment"
    return display(req, toiURL, news18URL, ddnewsURL, ndtvURL, title)


def display(req, toiURL, news18URL, ddnewsURL, ndtvURL, title):

    toi_news = toiS.get_articles(toiURL)
    n18_news = n18S.get_articles(news18URL.format(1))
    dd_news = get_dd_articles(ddnewsURL.format(1))
    ndtv_news = get_ndtv_articles(ndtvURL.format(1))

    for dd in dd_news:
        if dd["link"] == "#":
            dd_news.remove(dd)
        if dd["content"] == "":
            dd_news.remove(dd)
    for ndtv in ndtv_news:
        if ndtv["content"] == "":
            ndtv_news.remove(ndtv)
        else:
            print(ndtv['title'])
    return render(req, 'news/index.html',{'title':title, 'toi':toi_news, 'n18': n18_news, 'dd': dd_news, 'ndtv': ndtv_news})



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
